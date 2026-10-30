"""Deterministic source retrieval, preserving exact project-scoped line evidence."""
import re
from .store import InvalidInput

STOP = {'the','and','with','from','what','about','when','where','that','this','have','show','tell','into','your','how','are','was','why','for','can'}


def terms(question: str) -> list[str]:
    if not question.strip() or len(question) > 2000:
        raise InvalidInput('Question must be 1–2000 characters')
    return [x for x in re.findall(r'[\w]+', question.casefold()) if len(x)>2 and x not in STOP]


def search(store, project_id: str, question: str, limit: int = 8) -> dict:
    words = terms(question)
    if not 1 <= limit <= 25:
        raise InvalidInput('Limit must be 1–25')
    candidates=[]
    for source_meta in store.sources(project_id):
        if source_meta['status']!='active':
            continue
        source=store.source(project_id, source_meta['id'])
        lines=source['content'].splitlines()
        header=lines[0].casefold() if source['kind']=='csv' and lines else ''
        for lineno, line in enumerate(lines,1):
            folded=line.casefold()
            hits=sum(1 for word in set(words) if word in folded)
            if header and lineno>1 and hits:
                hits += sum(1 for word in set(words) if word in header and word not in folded)
            if hits:
                candidates.append((hits, {'source_id':source['id'], 'source_name':source['name'],
                    'sha256':source['sha256'], 'line':lineno, 'excerpt':line,
                    'origin':source['origin'], 'imported_at':source['imported_at']}))
    candidates.sort(key=lambda pair:(-pair[0],pair[1]['source_name'],pair[1]['line']))
    matches=[item for _,item in candidates[:limit]]
    return {'query':question,'matches':matches,'has_evidence':bool(matches),'mode':'literal-line-retrieval',
            'notice':'Results match source text. A match alone does not prove a political claim.'}


def research(store, project_id: str, question: str) -> dict:
    result=search(store,project_id,question)
    if not result['has_evidence']:
        answer='No matching evidence in the active sources of this project. No answer was inferred.'
    else:
        snippets=[f"[{i}] {m['excerpt'][:350]}" for i,m in enumerate(result['matches'],1)]
        answer='Matching source excerpts (not an AI-generated conclusion):\n'+'\n'.join(snippets)
    artifact=store.save_artifact(project_id,question,answer,result['matches'], generation_method='extractive' if result['has_evidence'] else 'no-evidence')
    return {'answer':answer,'artifact':artifact,'has_evidence':result['has_evidence'],
            'ai_generated':False,'model_status':'not-invoked','generation_method':artifact['generation_method']}


async def ai_research(store, project_id: str, question: str, mode: str = 'auto') -> dict:
    """AI-native research route: retrieve authoritative snippets before model generation.

    In auto mode, use the shared AI gateway when configured. If no model is
    configured, return a clearly labeled extractive artifact. Explicit AI mode
    never pretends source excerpts are an AI response.
    """
    from .ai import config, synthesize, AIUnavailable
    if mode not in {'auto', 'ai', 'extractive'}:
        raise InvalidInput('Research mode must be auto, ai or extractive')
    result = search(store, project_id, question)
    if not result['has_evidence']:
        artifact = store.save_artifact(project_id, question,
            'No matching evidence in this project. LiOS.Pol will not generate an unsupported political claim.',
            [], generation_method='no-evidence')
        return {'answer': artifact['answer'], 'artifact': artifact, 'has_evidence': False,
                'ai_generated': False, 'model_status': 'not-invoked-no-evidence', 'generation_method': 'no-evidence'}
    if mode == 'extractive' or (mode == 'auto' and not config().get('configured')):
        reply = research(store, project_id, question)
        reply['model_status'] = 'not-configured' if mode == 'auto' else 'not-requested'
        return reply
    answer, cited, model_id = await synthesize(question, result['matches'])
    # AI cited refs are exact verified source lines; the model cannot invent an
    # evidence ID or write model-generated source records.
    artifact = store.save_artifact(project_id, question, answer, cited,
                                   generation_method='ai-synthesis', model_id=model_id)
    return {'answer': answer, 'artifact': artifact, 'has_evidence': bool(cited),
            'ai_generated': True, 'model_status': 'completed', 'generation_method': 'ai-synthesis'}
