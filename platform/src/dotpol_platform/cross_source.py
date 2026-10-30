"""P1.07 source comparison using the existing local project search adapter.

No new search engine, hosted data or model-generated conclusions. Only exact
active source lines are stored as one canonical research artifact.
"""
from __future__ import annotations

from .research import search


def compare_sources(store, project_id: str, question: str) -> dict:
    result = search(store, project_id, question, limit=25)
    by_source: dict[str, list[dict]] = {}
    for hit in result['matches']:
        key = hit['source_id']
        by_source.setdefault(key, [])
        if len(by_source[key]) < 2:
            by_source[key].append(hit)
    selected = [hit for hits in list(by_source.values())[:6] for hit in hits]
    comparable = len(by_source) >= 2
    if not selected:
        answer = 'No matching source excerpts in this project. No comparison or conclusion was inferred.'
    elif not comparable:
        answer = ('Only one distinct source among retrieved excerpts. A cross-source comparison is not supported.\n'
                  'Matched excerpt (not an independently verified conclusion):\n'
                  + '\n'.join(f'[{i}] {hit["source_name"]}, line {hit["line"]}: {hit["excerpt"][:350]}'
                              for i, hit in enumerate(selected, 1)))
    else:
        answer = ('Cross-source excerpt matrix (distinct files do not prove source independence; no automated agreement or contradiction claim):\n'
                  + '\n'.join(f'[{i}] {hit["source_name"]}, line {hit["line"]}: {hit["excerpt"][:350]}'
                              for i, hit in enumerate(selected, 1))
                  + '\nInterpretation requires checking source independence, dates, definitions and methodologies.')
    artifact = store.save_artifact(project_id, question, answer, selected,
                                   generation_method='extractive' if selected else 'no-evidence')
    return {
        'answer': answer, 'artifact': artifact, 'comparison_ready': comparable,
        'source_count': len(by_source), 'ai_generated': False,
        'retrieval_mode': result['mode'], 'retrieval_degraded': result.get('degraded'),
    }
