"""P1.02 native SQLite backups preserve sources, artifacts, revisions and IDs."""
import hashlib
import pytest
from dotpol_platform.store import Store, InvalidInput
from dotpol_platform.backup import backup_store, verify_backup
from dotpol_platform.political_identity import initialize, register, list_entities


def test_backup_roundtrip_preserves_full_store(tmp_path):
    db = Store(tmp_path/'dotpol.sqlite3')
    initialize(db)
    p = db.create_project('Elections')['id']
    src = db.import_source(p, 'report.txt', 'txt', 'Aggregate public turnout 73 percent')
    art = db.save_artifact(p, 'turnout', 'Source reported 73 percent', [{
        'source_id':src['id'], 'source_name':src['name'], 'sha256':src['sha256'],
        'line':1, 'excerpt':'Aggregate public turnout 73 percent',
    }])
    db.revise_artifact(p,art['id'],'Human checked 73 percent',1)
    entity = register(db,p,'election','Election 2024',src['id'])
    with db._connect() as conn:
        conn.execute('PRAGMA journal_mode=WAL')
    snapshot = tmp_path/'export.sqlite3'
    out = backup_store(db, snapshot)
    assert out['verified'] and out['size_bytes'] > 0
    assert out['sha256'] == hashlib.sha256(snapshot.read_bytes()).hexdigest()
    assert verify_backup(snapshot)
    restored = Store(snapshot)
    initialize(restored)
    assert restored.project(p)['title'] == 'Elections'
    assert restored.source(p,src['id'])['content'] == 'Aggregate public turnout 73 percent'
    assert restored.artifact(p,art['id'])['revision'] == 2
    assert len(restored.artifact_history(p,art['id'])) == 2
    assert list_entities(restored,p)[0]['id'] == entity['id']


def test_non_overwrite_and_integrity_failure(tmp_path):
    db = Store(tmp_path/'live.sqlite3')
    initialize(db)
    with pytest.raises(InvalidInput):
        backup_store(db, db.db_path)
    out = tmp_path/'backup.sqlite3'
    backup_store(db,out)
    with pytest.raises(InvalidInput):
        backup_store(db,out)
    out.write_bytes(b'not a SQLite database')
    assert not verify_backup(out)
    with pytest.raises(InvalidInput):
        backup_store(db,tmp_path/'missing'/'backup.sqlite3')
