import hashlib
import importlib
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from dotpol_platform.store import Store, InvalidInput


def client(tmp_path):
    from app import create_app
    return TestClient(create_app(tmp_path/'data'/'local.sqlite3'))


def post(c,url,body):
    return c.post(url,json=body,headers={'X-Dotpol-Local':'1'})


def test_no_key_project_restart_and_provenance(tmp_path):
    c=client(tmp_path)
    assert c.get('/health').json()['status']=='ok'
    p=post(c,'/api/projects',{'title':'Public election research'}).json()
    content='constituency,votes\nNorth,125\nSouth,95'
    source=post(c,f"/api/projects/{p['id']}/sources",{'name':'synthetic.csv','kind':'csv','content':content,'origin':'synthetic-demo'}).json()
    assert source['sha256']==hashlib.sha256(content.encode()).hexdigest()
    ans=post(c,f"/api/projects/{p['id']}/research",{'question':'North votes'}).json()
    assert ans['has_evidence'] and not ans['ai_generated']
    assert ans['artifact']['evidence'][0]['line']==2
    assert ans['artifact']['evidence'][0]['excerpt']=='North,125'
    d=client(tmp_path)
    assert d.get(f"/api/projects/{p['id']}").json()['title']=='Public election research'
    assert d.get(f"/api/projects/{p['id']}/artifacts").json()[0]['id']==ans['artifact']['id']
    assert d.get(f"/api/projects/{p['id']}/sources/{source['id']}").json()['content']==content


def test_unknown_question_withdrawal_and_cross_project(tmp_path):
    c=client(tmp_path)
    p1=post(c,'/api/projects',{'title':'A'}).json()['id']
    p2=post(c,'/api/projects',{'title':'B'}).json()['id']
    s=post(c,f'/api/projects/{p1}/sources',{'name':'report.txt','kind':'txt','content':'river desilting verified'}).json()
    no=post(c,f'/api/projects/{p1}/research',{'question':'quantum gravity'}).json()
    assert not no['has_evidence'] and not no['artifact']['evidence']
    assert c.get(f"/api/projects/{p2}/sources/{s['id']}").status_code==404
    post(c,f"/api/projects/{p1}/sources/{s['id']}/withdraw",{})
    assert not c.get(f'/api/projects/{p1}/search',params={'q':'desilting'}).json()['has_evidence']
    with pytest.raises(InvalidInput):
        Store(tmp_path/'data'/'local.sqlite3').save_artifact(p1,'test','claim',[{'source_id':s['id'],'sha256':s['sha256'],'line':1,'excerpt':'river desilting verified'}])


def test_origin_csrf_host_and_invalid_inputs(tmp_path):
    c=client(tmp_path)
    assert c.post('/api/projects',json={'title':'bad'}).status_code==403
    assert post(c,'/api/projects',{'title':'bad'},).status_code==201
    assert c.get('/health',headers={'Host':'evil.example'}).status_code==403
    assert c.get('/health',headers={'Origin':'https://evil.example'}).status_code==403
    assert post(c,'/api/projects',{'title':' '}).status_code==422
    project=post(c,'/api/projects',{'title':'OK'}).json()['id']
    assert post(c,f'/api/projects/{project}/sources',{'name':'invalid.json','kind':'json','content':'{bad'}).status_code==422
    assert c.get('/api/projects/../../etc/passwd').status_code in {404,422}
    assert c.get(f'/api/projects/{project}/search',params={'q':'x'*2001}).status_code==422


def test_exact_citations_cannot_be_forged(tmp_path):
    store=Store(tmp_path/'db.sqlite3')
    p=store.create_project('Test')['id']
    s=store.import_source(p,'source.txt','txt','verified public record')
    for refs in ([{'source_id':s['id'],'sha256':s['sha256'],'line':2,'excerpt':'x'}],
                 [{'source_id':s['id'],'sha256':s['sha256'],'line':1,'excerpt':'invented claim'}]):
        with pytest.raises(InvalidInput):
            store.save_artifact(p,'Q','bad',refs)
    with pytest.raises(InvalidInput):
        store.import_source(p,'huge.txt','txt','x'*(1024*1024+1))


def test_ai_gateway_no_model_and_no_unverified_inference(tmp_path, monkeypatch):
    monkeypatch.delenv('DOTPOL_AI_MODEL', raising=False)
    monkeypatch.delenv('DOTPOL_AI_PROVIDER', raising=False)
    c=client(tmp_path)
    project=post(c,'/api/projects',{'title':'Psephology research'}).json()
    post(c,f"/api/projects/{project['id']}/sources",{'name':'report.txt','kind':'txt','content':'Official aggregate turnout 73 percent'})
    response=post(c,f"/api/projects/{project['id']}/research",{'question':'turnout'})
    assert response.status_code==200
    assert response.json()['ai_generated'] is False
    assert response.json()['artifact']['generation_method']=='extractive'
    assert post(c,f"/api/projects/{project['id']}/research",{'question':'turnout','mode':'ai'}).status_code==503
    assert post(c,f"/api/projects/{project['id']}/research",{'question':'unsupported individual prediction'}).json()['generation_method']=='no-evidence'


def test_ai_grounded_answer_validated_and_persisted(tmp_path, monkeypatch):
    from dotpol_platform import ai
    monkeypatch.setenv('DOTPOL_AI_MODEL','qwen3:1.7b')
    monkeypatch.setenv('DOTPOL_AI_PROVIDER','ollama')
    class Result:
        output='The reported aggregate turnout is 73 percent [1].'
    class FakeAgent:
        async def run(self, prompt):
            assert 'Official turnout 73 percent' in prompt
            assert 'UNTRUSTED' in prompt
            return Result()
    monkeypatch.setattr(ai,'_make_agent',lambda cfg: FakeAgent())
    c=client(tmp_path)
    project=post(c,'/api/projects',{'title':'Political research'}).json()
    post(c,f"/api/projects/{project['id']}/sources",{'name':'election.txt','kind':'txt','content':'Official turnout 73 percent'})
    response=post(c,f"/api/projects/{project['id']}/research",{'question':'turnout','mode':'ai'})
    assert response.status_code==200
    payload=response.json()
    assert payload['ai_generated'] is True
    assert payload['artifact']['generation_method']=='ai-synthesis'
    assert payload['artifact']['model_id']=='ollama:qwen3:1.7b'
    assert payload['artifact']['evidence'][0]['line']==1
    assert c.get(f"/api/projects/{project['id']}/artifacts").json()[0]['model_id']=='ollama:qwen3:1.7b'


def test_ai_invalid_citation_is_rejected_and_not_saved(tmp_path, monkeypatch):
    from dotpol_platform import ai
    monkeypatch.setenv('DOTPOL_AI_MODEL','testmodel')
    monkeypatch.setenv('DOTPOL_AI_PROVIDER','ollama')
    class FakeAgent:
        async def run(self, prompt):
            class Result:
                output='Invented election statement [99].'
            return Result()
    monkeypatch.setattr(ai,'_make_agent',lambda cfg: FakeAgent())
    c=client(tmp_path)
    p=post(c,'/api/projects',{'title':'Political research'}).json()['id']
    post(c,f'/api/projects/{p}/sources',{'name':'report.txt','kind':'txt','content':'Verified aggregate turnout report'})
    response=post(c,f'/api/projects/{p}/research',{'question':'turnout','mode':'ai'})
    assert response.status_code==422
    assert c.get(f'/api/projects/{p}/artifacts').json()==[]


def test_ai_provider_config_disallows_remote_ollama_and_missing_byoai_key(monkeypatch):
    from dotpol_platform.ai import config
    monkeypatch.setenv('DOTPOL_AI_PROVIDER','ollama')
    monkeypatch.setenv('DOTPOL_AI_MODEL','qwen3')
    monkeypatch.setenv('DOTPOL_OLLAMA_URL','https://some-remote-server.example')
    assert config()['status']=='invalid-configuration'
    monkeypatch.setenv('DOTPOL_AI_PROVIDER','openai-compatible')
    monkeypatch.setenv('DOTPOL_AI_API_BASE','http://example.com')
    monkeypatch.setenv('DOTPOL_AI_API_KEY','PRIVATE_SECRET')
    assert config()['status']=='invalid-configuration'
    monkeypatch.setenv('DOTPOL_AI_API_BASE','https://example.com/v1')
    monkeypatch.delenv('DOTPOL_AI_API_KEY')
    assert config()['status']=='model-not-configured'
    assert 'PRIVATE_SECRET' not in repr(config())
