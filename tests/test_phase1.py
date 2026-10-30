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
