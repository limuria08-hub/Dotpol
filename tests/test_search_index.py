"""Source authority and index invalidation checks for P1 retrieval."""
from dotpol_platform.store import Store
from dotpol_platform.research import search


def test_literal_fallback_truthful_and_project_scoped(tmp_path, monkeypatch):
    monkeypatch.setenv('DOTPOL_SEARCH_ENGINE', 'literal')
    db = Store(tmp_path/'data'/'db.sqlite3')
    p = db.create_project('Public-source review')['id']
    other = db.create_project('Other research')['id']
    src = db.import_source(p, 'report.txt', 'txt', 'Budget allocation 100 crores\nWater scheme report')
    result = search(db, p, 'budget allocation')
    assert result['mode'] == 'literal-line-retrieval'
    assert result['matches'][0]['source_id'] == src['id']
    assert not search(db, other, 'budget allocation')['has_evidence']
    db.withdraw(p, src['id'])
    assert not search(db, p, 'budget allocation')['has_evidence']


def test_auto_fallback_never_fabricates_evidence(tmp_path, monkeypatch):
    from dotpol_platform import search_index
    monkeypatch.setenv('DOTPOL_SEARCH_ENGINE', 'auto')
    db = Store(tmp_path/'db.sqlite3')
    p = db.create_project('Research')['id']
    db.import_source(p, 'issue.txt', 'txt', 'Verified aggregate public service issue')
    def unavailable(*args):
        raise search_index.SearchIndexUnavailable('Not installed')
    monkeypatch.setattr(search_index, 'search_fts', unavailable)
    result = search(db, p, 'service issue')
    assert result['mode'] == 'literal-line-retrieval' and result['degraded']
    assert result['matches'][0]['excerpt'] == 'Verified aggregate public service issue'
    assert not search(db, p, 'unanswerable') ['has_evidence']


def test_lancedb_fts_index_rebuild_and_withdrawal(tmp_path, monkeypatch):
    import pytest
    pytest.importorskip('lancedb')
    monkeypatch.setenv('DOTPOL_SEARCH_ENGINE', 'lancedb')
    db = Store(tmp_path/'data'/'db.sqlite3')
    p = db.create_project('Research')['id']
    other = db.create_project('Other')['id']
    s = db.import_source(p, 'scheme.txt', 'txt', 'River restoration implementation\nWater budget')
    assert search(db, p, 'restoration')['mode'] == 'lancedb-fts'
    assert search(db, p, 'restoration')['matches'][0]['source_id'] == s['id']
    assert not search(db, other, 'restoration')['has_evidence']
    db.withdraw(p, s['id'])
    assert not search(db, p, 'restoration')['has_evidence']
    assert search(db, p, 'restoration')['mode'] == 'lancedb-fts'
