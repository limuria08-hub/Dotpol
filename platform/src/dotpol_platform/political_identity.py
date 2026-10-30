"""P1.10 canonical political identities in the existing local SQLite store.

Registered labels are user-declared and unverified. Full election entities,
relations, time-valid boundaries, and assertion resolution belong to P2/P3.
"""
from __future__ import annotations

import sqlite3
from .store import Store, InvalidInput, NotFound, identifier, now

KINDS = frozenset({
    "jurisdiction", "administrative-area", "electoral-area", "constituency",
    "boundary-version", "polling-station", "person", "party", "alliance",
    "organisation", "office", "election", "contest",
})


def initialize(store: Store) -> None:
    """Repeatable, non-destructive migration in the ONE canonical database."""
    with store._connect() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS political_entities (
            id TEXT PRIMARY KEY,
            project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
            kind TEXT NOT NULL,
            name TEXT NOT NULL,
            canonical_key TEXT NOT NULL,
            source_id TEXT REFERENCES sources(id) ON DELETE RESTRICT,
            source_sha256 TEXT,
            version INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'user-declared-unverified',
            UNIQUE(project_id,kind,canonical_key)
        )""")
        db.execute("""CREATE INDEX IF NOT EXISTS idx_political_entities_project_kind
                      ON political_entities(project_id,kind)""")


def _public(row) -> dict:
    return {key: value for key, value in dict(row).items() if key != "canonical_key"}


def register(store: Store, project_id: str, kind: str, name: str,
             source_id: str | None = None) -> dict:
    store.project(project_id)
    if kind not in KINDS:
        raise InvalidInput("Unknown political entity kind")
    if not isinstance(name, str):
        raise InvalidInput("Political entity name must be 1–180 characters")
    name = " ".join(name.split())
    if not 1 <= len(name) <= 180:
        raise InvalidInput("Political entity name must be 1–180 characters")
    if source_id is not None:
        store._check_id(source_id)
    with store._connect() as db:
        db.execute("BEGIN IMMEDIATE")
        source_sha256 = None
        if source_id:
            source = db.execute(
                "SELECT sha256,status FROM sources WHERE id=? AND project_id=?",
                (source_id, project_id),
            ).fetchone()
            if source is None or source["status"] != "active":
                raise InvalidInput("Entity source must be active in the same project")
            source_sha256 = source["sha256"]
        record = dict(
            id=identifier(), project_id=project_id, kind=kind, name=name,
            canonical_key=name.casefold(), source_id=source_id,
            source_sha256=source_sha256, version=1, created_at=now(),
            status="user-declared-unverified",
        )
        try:
            db.execute("""INSERT INTO political_entities
                (id,project_id,kind,name,canonical_key,source_id,source_sha256,version,created_at,status)
                VALUES (:id,:project_id,:kind,:name,:canonical_key,:source_id,:source_sha256,:version,:created_at,:status)""", record)
        except sqlite3.IntegrityError as exc:
            raise InvalidInput("Duplicate political entity of the same kind/name in project") from exc
    return _public(record)


def list_entities(store: Store, project_id: str, kind: str | None = None) -> list[dict]:
    store.project(project_id)
    if kind is not None and kind not in KINDS:
        raise InvalidInput("Unknown political entity kind")
    with store._connect() as db:
        if kind is None:
            rows = db.execute("SELECT * FROM political_entities WHERE project_id=? ORDER BY created_at,id", (project_id,))
        else:
            rows = db.execute("SELECT * FROM political_entities WHERE project_id=? AND kind=? ORDER BY created_at,id", (project_id,kind))
        return [_public(row) for row in rows]


def get_entity(store: Store, project_id: str, entity_id: str) -> dict:
    store.project(project_id)
    store._check_id(entity_id)
    with store._connect() as db:
        row = db.execute(
            "SELECT * FROM political_entities WHERE id=? AND project_id=?",
            (entity_id, project_id),
        ).fetchone()
    if row is None:
        raise NotFound("Political entity not found in project")
    return _public(row)
