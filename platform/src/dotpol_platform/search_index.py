"""Local-only LanceDB full-text adapter for evidence retrieval.

SQLite remains the source of truth. LanceDB is a disposable index of active
source lines; every result is checked against current canonical source bytes.
Embedding/vector search is deliberately NOT claimed by this adapter.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path


class SearchIndexUnavailable(RuntimeError):
    """Optional index missing or unusable; safe literal retrieval remains available."""


def _index_manifest(sources: list[dict]) -> str:
    canonical = sorted((s['id'], s['sha256'], s['status']) for s in sources)
    return hashlib.sha256(json.dumps(canonical, separators=(',', ':')).encode()).hexdigest()


def search_fts(store, project_id: str, query: str, limit: int) -> list[dict]:
    """Return validated active source lines using local LanceDB BM25 FTS.

    Always verify returned hits using authoritative SQLite content/checksums.
    Never trust an index to grant project access or validate citations.
    """
    if importlib.util.find_spec('lancedb') is None:
        raise SearchIndexUnavailable('LanceDB is not installed')
    try:
        import lancedb
        from lancedb.index import FTS

        # project() validates the ID. The folder is a derivative cache and
        # never receives an externally supplied filesystem path.
        store.project(project_id)
        metadata = store.sources(project_id)
        live = [s for s in metadata if s['status'] == 'active']
        if not live:
            return []
        fingerprint = _index_manifest(metadata)
        root = (Path(store.db_path).parent / 'search-index' / project_id)
        root.mkdir(parents=True, exist_ok=True)
        manifest_path = root / 'manifest.json'
        db = lancedb.connect(str(root / 'lance'))
        table_name = 'source_lines'
        ready = False
        if manifest_path.exists():
            try:
                ready = json.loads(manifest_path.read_text(encoding='utf-8')).get('fingerprint') == fingerprint and table_name in db.table_names()
            except (OSError, ValueError, TypeError):
                ready = False
        if not ready:
            lines = []
            for meta in live:
                source = store.source(project_id, meta['id'])
                for number, excerpt in enumerate(source['content'].splitlines(), 1):
                    if excerpt.strip():
                        lines.append({'source_id': source['id'], 'sha256': source['sha256'],
                                      'line': number, 'text': excerpt})
            if not lines:
                return []
            table = db.create_table(table_name, data=lines, mode='overwrite')
            table.create_index('text', config=FTS())
            manifest_path.write_text(json.dumps({'fingerprint': fingerprint}), encoding='utf-8')
        else:
            table = db.open_table(table_name)

        # We use an FTS-specific query; there is no implicit/remote embedding.
        indexed_hits = table.search(query, query_type='fts').limit(min(100, max(25, limit * 5))).to_list()
        valid = []
        sources_by_id = {s['id']: s for s in live}
        for hit in indexed_hits:
            meta = sources_by_id.get(hit.get('source_id'))
            if meta is None or meta['sha256'] != hit.get('sha256'):
                continue
            original = store.source(project_id, meta['id'])
            if original['status'] != 'active' or original['sha256'] != meta['sha256']:
                continue
            number = hit.get('line')
            lines = original['content'].splitlines()
            if not isinstance(number, int) or not 1 <= number <= len(lines) or lines[number - 1] != hit.get('text'):
                continue
            valid.append({'source_id': meta['id'], 'source_name': meta['name'],
                          'sha256': meta['sha256'], 'line': number, 'excerpt': lines[number - 1],
                          'origin': meta['origin'], 'imported_at': meta['imported_at']})
            if len(valid) >= limit:
                break
        return valid
    except SearchIndexUnavailable:
        raise
    except Exception as exc:
        # FTS is optional. Never report a failed index query as verified retrieval.
        raise SearchIndexUnavailable('LanceDB index could not be used') from exc
