"""P1.10 canonical ID registration is local, evidence-bound and project-scoped."""
import hashlib
import pytest
from fastapi.testclient import TestClient
from app import create_app
from dotpol_platform.store import Store, InvalidInput, NotFound
from dotpol_platform.political_identity import initialize, register, list_entities, get_entity


def test_registry_same_database_stable_id_restart(tmp_path):
    path = tmp_path/'dotpol.sqlite3'
    store = Store(path)
    initialize(store)
    project = store.create_project('Public politics research')['id']
    src = store.import_source(project, 'party.txt', 'txt', 'Synthetic party source')
    ent = register(store, project, 'party', '  Example    Party ', src['id'])
    assert ent['name'] == 'Example Party'
    assert ent['source_sha256'] == hashlib.sha256(b'Synthetic party source').hexdigest()
    assert ent['status'] == 'user-declared-unverified' and ent['version'] == 1
    initialize(Store(path))
    assert get_entity(Store(path), project, ent['id']) == ent
    assert list_entities(Store(path), project, 'party') == [ent]
    with pytest.raises(InvalidInput):
        register(store, project, 'party', 'EXAMPLE party')
    register(store, project, 'organisation', 'Example Party')


def test_identity_project_scope_and_withdrawn_source(tmp_path):
    db = Store(tmp_path/'db.sqlite3')
    initialize(db)
    a = db.create_project('A')['id']
    b = db.create_project('B')['id']
    src = db.import_source(a, 'source.txt', 'txt', 'Synthetic historical data')
    ent = register(db, a, 'constituency', 'West', src['id'])
    assert list_entities(db,b) == []
    with pytest.raises(NotFound):
        get_entity(db,b,ent['id'])
    with pytest.raises(InvalidInput):
        register(db,b,'election','General',src['id'])
    db.withdraw(a,src['id'])
    assert get_entity(db,a,ent['id'])['source_sha256'] == src['sha256']
    with pytest.raises(InvalidInput):
        register(db,a,'party','Other',src['id'])


def test_reject_private_inference_and_invalid_labels(tmp_path):
    db = Store(tmp_path/'db.sqlite3')
    initialize(db)
    p = db.create_project('P')['id']
    for kind in ['supporter-score','voter-political-preference','household-target']:
        with pytest.raises(InvalidInput):
            register(db,p,kind,'Example')
    for name in ['', '  ', 'x'*181]:
        with pytest.raises(InvalidInput):
            register(db,p,'party',name)
    with pytest.raises(InvalidInput):
        register(db,p,'election','Reference','not-a-uuid')


def test_api_entity_roundtrip_and_local_scope(tmp_path):
    c = TestClient(create_app(tmp_path/'db.sqlite3'))
    h={'X-Dotpol-Local':'1'}
    p=c.post('/api/projects',json={'title':'Registry'},headers=h).json()['id']
    r=c.post(f'/api/projects/{p}/entities',json={'kind':'jurisdiction','name':'  Test State  '},headers=h)
    assert r.status_code==201, r.text
    eid=r.json()['id']
    assert c.get(f'/api/projects/{p}/entities/{eid}').json()['name']=='Test State'
    assert len(c.get(f'/api/projects/{p}/entities?kind=jurisdiction').json())==1
    assert c.post(f'/api/projects/{p}/entities',json={'kind':'jurisdiction','name':'test STATE'},headers=h).status_code==422
    assert c.post(f'/api/projects/{p}/entities',json={'kind':'party','name':'No origin'},headers={'Origin':'https://evil.test',**h}).status_code==403
    assert c.post(f'/api/projects/{p}/entities',json={'kind':'party','name':'No origin'}).status_code==403
