"""P1.07 independently sourced comparison, no fabricated source conflicts."""
from fastapi.testclient import TestClient
from app import create_app
from dotpol_platform.store import Store
from dotpol_platform.cross_source import compare_sources


def test_compares_distinct_project_sources_with_exact_refs(tmp_path, monkeypatch):
    monkeypatch.setenv('DOTPOL_SEARCH_ENGINE','literal')
    db=Store(tmp_path/'d.sqlite3')
    p=db.create_project('Public data')['id']
    a=db.import_source(p,'one.txt','txt','Reported water budget 120 units')
    b=db.import_source(p,'two.txt','txt','Water budget report from fiscal audit: 130 units')
    got=compare_sources(db,p,'water budget')
    assert got['comparison_ready'] and got['source_count']==2
    assert not got['ai_generated']
    assert {x['source_id'] for x in got['artifact']['evidence']}=={a['id'],b['id']}
    assert 'no automated agreement or contradiction' in got['answer']
    assert db.artifact(p,got['artifact']['id'])['id']==got['artifact']['id']
    db.withdraw(p,b['id'])
    fewer=compare_sources(db,p,'water budget')
    assert not fewer['comparison_ready'] and fewer['source_count']==1
    assert b['id'] not in {x['source_id'] for x in fewer['artifact']['evidence']}


def test_comparison_no_evidence_and_cross_project(tmp_path,monkeypatch):
    monkeypatch.setenv('DOTPOL_SEARCH_ENGINE','literal')
    db=Store(tmp_path/'db.sqlite3')
    a=db.create_project('A')['id']
    b=db.create_project('B')['id']
    db.import_source(a,'x.txt','txt','Public scheme budget 5')
    out=compare_sources(db,b,'scheme budget')
    assert not out['comparison_ready'] and not out['artifact']['evidence']
    assert out['artifact']['generation_method']=='no-evidence'


def test_comparison_api_creates_one_scoped_artifact(tmp_path,monkeypatch):
    monkeypatch.setenv('DOTPOL_SEARCH_ENGINE','literal')
    c=TestClient(create_app(tmp_path/'db.sqlite3'))
    h={'X-Dotpol-Local':'1'}
    p=c.post('/api/projects',json={'title':'Research'},headers=h).json()['id']
    for i in [1,2]:
        r=c.post(f'/api/projects/{p}/sources',json={'name':f's{i}.txt','kind':'txt','content':f'Synthetic public budget {i}'},headers=h)
        assert r.status_code==201
    q=c.post(f'/api/projects/{p}/compare',headers=h,json={'question':'public budget'})
    assert q.status_code==200,q.text
    assert q.json()['source_count']==2
    assert q.json()['artifact']['id']==c.get(f'/api/projects/{p}/artifacts').json()[0]['id']
    assert c.post(f'/api/projects/{p}/compare',json={'question':'budget'}).status_code==403
    assert c.post(f'/api/projects/{p}/compare',headers={**h,'Origin':'https://evil.example'},json={'question':'budget'}).status_code==403
