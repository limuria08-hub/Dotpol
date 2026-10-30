"""P1.09: the editable workbench owns one canonical Artifact ID."""
import sqlite3

from fastapi.testclient import TestClient

from dotpol_platform.store import Store


def client(tmp_path):
    from app import create_app
    return TestClient(create_app(tmp_path / "dotpol.sqlite3"))


def post(c, path, body):
    return c.post(path, json=body, headers={"X-Dotpol-Local": "1"})


def test_edit_reopen_history_and_optimistic_conflict(tmp_path, monkeypatch):
    monkeypatch.delenv("DOTPOL_AI_MODEL", raising=False)
    monkeypatch.delenv("DOTPOL_AI_PROVIDER", raising=False)
    c = client(tmp_path)
    project = post(c, "/api/projects", {"title": "Local research"}).json()
    base = f"/api/projects/{project['id']}"
    src = post(c, base + "/sources", {
        "name": "policy.txt", "kind": "txt",
        "content": "The report dates from 2026.\nThe budget was 100 units.",
    }).json()
    initial = post(c, base + "/research", {
        "question": "budget", "mode": "extractive"
    }).json()["artifact"]
    artifact_id = initial["id"]
    endpoint = f"{base}/artifacts/{artifact_id}"
    assert initial["revision"] == 1
    assert initial["last_editor"] == "original"

    edited = post(c, endpoint + "/revisions", {
        "answer": "Edited by a researcher. Verify claims against the linked line.",
        "expected_revision": 1,
    })
    assert edited.status_code == 200
    revised = edited.json()
    assert revised["id"] == artifact_id
    assert revised["revision"] == 2
    assert revised["last_editor"] == "human"
    assert revised["generation_method"] == "extractive"  # original provenance
    assert revised["evidence"] == initial["evidence"]
    assert revised["evidence"][0]["source_id"] == src["id"]
    assert revised["answer"].startswith("Edited by a researcher")

    history = c.get(endpoint + "/revisions").json()
    assert [r["revision"] for r in history] == [1, 2]
    assert [r["editor_kind"] for r in history] == ["original", "human"]
    assert history[0]["answer"] == initial["answer"]
    assert history[1]["answer"] == revised["answer"]

    stale = post(c, endpoint + "/revisions", {
        "answer": "An outdated tab should not overwrite the edit.",
        "expected_revision": 1,
    })
    assert stale.status_code == 409
    assert stale.json()["status"] == "revision-conflict"
    assert len(c.get(endpoint + "/revisions").json()) == 2

    reopened = client(tmp_path)
    assert reopened.get(endpoint).json()["revision"] == 2
    assert reopened.get(base + "/artifacts").json()[0]["id"] == artifact_id
    assert reopened.get(endpoint + "/revisions").json()[0]["answer"] == initial["answer"]

    again = post(reopened, endpoint + "/revisions", {
        "answer": "Reviewed and amended a second time.",
        "expected_revision": 2,
    })
    assert again.status_code == 200
    assert again.json()["revision"] == 3
    assert len(reopened.get(endpoint + "/revisions").json()) == 3

    # Unchanged content is not a new revision.
    unchanged = post(reopened, endpoint + "/revisions", {
        "answer": "Reviewed and amended a second time.", "expected_revision": 3,
    })
    assert unchanged.status_code == 200 and unchanged.json()["revision"] == 3
    assert len(reopened.get(endpoint + "/revisions").json()) == 3


def test_revision_validation_scope_and_local_request_guard(tmp_path):
    c = client(tmp_path)
    p1 = post(c, "/api/projects", {"title": "Research A"}).json()["id"]
    p2 = post(c, "/api/projects", {"title": "Research B"}).json()["id"]
    post(c, f"/api/projects/{p1}/sources", {
        "name": "brief.txt", "kind": "txt", "content": "A published budget statement."
    })
    artifact = post(c, f"/api/projects/{p1}/research", {
        "question": "budget", "mode": "extractive"
    }).json()["artifact"]
    endpoint = f"/api/projects/{p1}/artifacts/{artifact['id']}/revisions"
    assert c.post(endpoint, json={"answer": "edit", "expected_revision": 1}).status_code == 403
    assert post(c, endpoint, {"answer": "  ", "expected_revision": 1}).status_code == 422
    assert post(c, endpoint, {"answer": "valid", "expected_revision": 0}).status_code == 422
    assert post(c, endpoint, {"answer": "valid", "expected_revision": True}).status_code == 422
    assert post(c, endpoint, {"answer": "x" * 100001, "expected_revision": 1}).status_code == 422
    assert post(c, endpoint, {"answer": "🌐" * 30000, "expected_revision": 1}).status_code == 422  # UTF-8 byte limit
    other = f"/api/projects/{p2}/artifacts/{artifact['id']}/revisions"
    assert c.get(other).status_code == 404
    assert post(c, other, {"answer": "bad scope", "expected_revision": 1}).status_code == 404
    assert c.get(endpoint).json()[0]["revision"] == 1


def test_preexisting_database_is_migrated_without_losing_original_answer(tmp_path):
    db_path = tmp_path / "old.sqlite3"
    project_id, artifact_id = "a" * 32, "b" * 32
    with sqlite3.connect(db_path) as db:
        db.executescript("""
            CREATE TABLE projects (id TEXT PRIMARY KEY, title TEXT NOT NULL,
                                   created_at TEXT NOT NULL);
            CREATE TABLE artifacts (
                id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                question TEXT NOT NULL, answer TEXT NOT NULL, evidence_json TEXT NOT NULL,
                created_at TEXT NOT NULL, generation_method TEXT NOT NULL DEFAULT 'extractive',
                model_id TEXT
            );
        """)
        db.execute("INSERT INTO projects VALUES (?,?,?)", (project_id, "Legacy", "2026-01-01"))
        db.execute(
            "INSERT INTO artifacts VALUES (?,?,?,?,?,?,?,?)",
            (artifact_id, project_id, "Original question", "Original answer", "[]",
             "2026-01-01", "extractive", None),
        )
    store = Store(db_path)
    original = store.artifact(project_id, artifact_id)
    assert original["revision"] == 1
    assert original["updated_at"] == "2026-01-01"
    assert store.artifact_revisions(project_id, artifact_id)[0]["answer"] == "Original answer"
    revised = store.revise_artifact(project_id, artifact_id, "Later correction", 1)
    assert revised["id"] == artifact_id and revised["revision"] == 2
    Store(db_path)  # migration must be idempotent
    assert len(store.artifact_revisions(project_id, artifact_id)) == 2
