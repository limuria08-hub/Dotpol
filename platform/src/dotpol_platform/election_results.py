"""P2.01/P2.02: source-linked candidate result imports into Dotpol's ONE SQLite DB.

This consumes user-imported, normalized CSV from the P1 source registry. It
does not scrape ECI, infer party aliases or personal beliefs, certify official
results, or create a competing datastore. IDs reuse P1 political_identity.
"""
from __future__ import annotations

import csv
import io
import re
import sqlite3
from collections import defaultdict
from .store import Store, InvalidInput, NotFound, identifier, now
from .political_identity import initialize as init_identities

SCHEMA = "dotpol-candidate-results-v1"
COLUMNS = (
    "election", "year", "constituency", "boundary_version",
    "candidate", "party", "votes", "total_valid_votes",
)
MAX_ROWS = 10_000
MAX_VOTES = (1 << 63) - 1


def initialize(store: Store) -> None:
    """Idempotent migration in the existing operational database."""
    init_identities(store)
    with store._connect() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS election_result_imports (
                id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                source_id TEXT NOT NULL REFERENCES sources(id) ON DELETE RESTRICT,
                source_sha256 TEXT NOT NULL,
                schema_version TEXT NOT NULL,
                imported_at TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'user-uploaded-unverified',
                UNIQUE(project_id,source_id)
            );
            CREATE TABLE IF NOT EXISTS election_candidate_results (
                id TEXT PRIMARY KEY,
                import_id TEXT NOT NULL REFERENCES election_result_imports(id) ON DELETE CASCADE,
                source_line INTEGER NOT NULL,
                election_id TEXT NOT NULL REFERENCES political_entities(id),
                constituency_id TEXT NOT NULL REFERENCES political_entities(id),
                boundary_version_id TEXT NOT NULL REFERENCES political_entities(id),
                party_id TEXT NOT NULL REFERENCES political_entities(id),
                candidate_name TEXT NOT NULL,
                year INTEGER NOT NULL,
                votes INTEGER NOT NULL CHECK(votes >= 0),
                total_valid_votes INTEGER NOT NULL CHECK(total_valid_votes > 0),
                UNIQUE(import_id,source_line)
            );
            CREATE INDEX IF NOT EXISTS idx_election_results_import
                ON election_candidate_results(import_id);
        """)


def _label(value: str | None, field: str) -> str:
    if not isinstance(value, str):
        raise InvalidInput(f"{field} must be text")
    v = " ".join(value.strip().split())
    if not 1 <= len(v) <= 180 or any(ord(ch) < 32 for ch in v):
        raise InvalidInput(f"{field} must be 1–180 printable characters")
    return v


def _integer(value: str | None, field: str, *, positive: bool = False) -> int:
    if not isinstance(value, str) or not re.fullmatch(r"(0|[1-9][0-9]*)", value.strip(), re.ASCII):
        raise InvalidInput(f"{field} must be a nonnegative base-10 integer")
    number = int(value)
    if number > MAX_VOTES or (positive and number == 0):
        raise InvalidInput(f"{field} exceeds its allowed integer range")
    return number


def parse_csv(content: str) -> list[dict]:
    """Validate all rows before mutating storage; preserve physical CSV lines."""
    try:
        reader = csv.DictReader(io.StringIO(content, newline=""), strict=True)
        if reader.fieldnames != list(COLUMNS):
            raise InvalidInput(f"Normalized CSV columns must be exactly: {', '.join(COLUMNS)}")
        parsed = []
        seen_candidates = set()
        totals = {}
        boundary_by_contest = {}
        sums = defaultdict(int)
        for record in reader:
            if len(parsed) >= MAX_ROWS:
                raise InvalidInput("Maximum 10000 candidate rows per imported source")
            if None in record or any(record.get(k) is None for k in COLUMNS):
                raise InvalidInput("CSV row has missing or unexpected fields")
            election = _label(record["election"], "election")
            constituency = _label(record["constituency"], "constituency")
            boundary = _label(record["boundary_version"], "boundary_version")
            candidate = _label(record["candidate"], "candidate")
            party = _label(record["party"], "party")
            year = _integer(record["year"], "year", positive=True)
            if not 1800 <= year <= 2200:
                raise InvalidInput("year must be between 1800 and 2200")
            votes = _integer(record["votes"], "votes")
            total = _integer(record["total_valid_votes"], "total_valid_votes", positive=True)
            if votes > total:
                raise InvalidInput("A candidate cannot exceed the declared contest total")
            contest = (election.casefold(), year, constituency.casefold())
            old_boundary = boundary_by_contest.setdefault(contest, boundary.casefold())
            if old_boundary != boundary.casefold():
                raise InvalidInput("Conflicting boundary versions for one election contest")
            old_total = totals.setdefault(contest, total)
            if old_total != total:
                raise InvalidInput("Inconsistent total_valid_votes within one contest")
            candidate_key = (*contest, candidate.casefold())
            if candidate_key in seen_candidates:
                raise InvalidInput("Duplicate candidate row in one contest")
            seen_candidates.add(candidate_key)
            sums[contest] += votes
            if sums[contest] > total:
                raise InvalidInput("Candidate sums exceed the declared contest total")
            parsed.append({
                "source_line": reader.line_num, "election": election, "year": year,
                "constituency": constituency, "boundary_version": boundary,
                "candidate": candidate, "party": party,
                "votes": votes, "total_valid_votes": total,
            })
    except csv.Error as exc:
        raise InvalidInput("Malformed normalized election CSV") from exc
    if not parsed:
        raise InvalidInput("Election result CSV contains no candidate rows")
    return parsed


def _id_for(db: sqlite3.Connection, project_id: str, kind: str,
            name: str, source_id: str, sha: str) -> str:
    key = name.casefold()
    row = db.execute(
        "SELECT id FROM political_entities WHERE project_id=? AND kind=? AND canonical_key=?",
        (project_id, kind, key),
    ).fetchone()
    if row is not None:
        return row["id"]
    entity_id = identifier()
    db.execute("""INSERT INTO political_entities
        (id,project_id,kind,name,canonical_key,source_id,source_sha256,version,created_at,status)
        VALUES (?,?,?,?,?,?,?,1,?,'user-declared-unverified')""",
        (entity_id, project_id, kind, name, key, source_id, sha, now()),
    )
    return entity_id


def _quality(rows: list[dict]) -> dict:
    contests = {}
    for row in rows:
        key = (row["election_id"], row["constituency_id"], row["year"])
        item = contests.setdefault(key, {
            "election_id": row["election_id"],
            "constituency_id": row["constituency_id"],
            "boundary_version_id": row["boundary_version_id"],
            "year": row["year"], "candidate_rows": 0,
            "reported_votes": 0, "declared_total_valid_votes": row["total_valid_votes"],
        })
        item["candidate_rows"] += 1
        item["reported_votes"] += row["votes"]
    for item in contests.values():
        item["unrepresented_votes"] = item["declared_total_valid_votes"] - item["reported_votes"]
        item["complete_against_declared_total"] = item["unrepresented_votes"] == 0
        # This checks the imported file's own arithmetic, NOT official results.
    return {"contest_count": len(contests), "candidate_row_count": len(rows),
            "contests": list(contests.values()), "source_verified": False,
            "official_status": "not-verified-from-primary-source"}


def import_results(store: Store, project_id: str, source_id: str) -> dict:
    """Atomic normalized candidate CSV import with original line/hash linkage."""
    store.project(project_id)
    source = store.source(project_id, source_id)
    if source["kind"] != "csv" or source["status"] != "active":
        raise InvalidInput("Use an active project CSV source for election result import")
    rows = parse_csv(source["content"])
    with store._connect() as db:
        db.execute("BEGIN IMMEDIATE")
        current = db.execute(
            "SELECT sha256,status,kind FROM sources WHERE project_id=? AND id=?",
            (project_id, source_id),
        ).fetchone()
        if (current is None or current["status"] != "active" or
                current["kind"] != "csv" or current["sha256"] != source["sha256"]):
            raise InvalidInput("Election source changed or was withdrawn during import")
        if db.execute("SELECT id FROM election_result_imports WHERE project_id=? AND source_id=?",
                      (project_id, source_id)).fetchone():
            raise InvalidInput("This source was already imported; create a new source version")
        import_id = identifier()
        db.execute("""INSERT INTO election_result_imports
            (id,project_id,source_id,source_sha256,schema_version,imported_at,status)
            VALUES (?,?,?,?,?,?,'user-uploaded-unverified')""",
            (import_id, project_id, source_id, source["sha256"], SCHEMA, now()),
        )
        for row in rows:
            election_id = _id_for(db, project_id, "election",
                                 f'{row["election"]} ({row["year"]})', source_id, source["sha256"])
            constituency_id = _id_for(db, project_id, "constituency",
                                     row["constituency"], source_id, source["sha256"])
            boundary_id = _id_for(db, project_id, "boundary-version",
                                  f'{row["constituency"]} / {row["boundary_version"]}',
                                  source_id, source["sha256"])
            party_id = _id_for(db, project_id, "party", row["party"], source_id, source["sha256"])
            db.execute("""INSERT INTO election_candidate_results
                (id,import_id,source_line,election_id,constituency_id,boundary_version_id,
                 party_id,candidate_name,year,votes,total_valid_votes)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (identifier(), import_id, row["source_line"], election_id,
                 constituency_id, boundary_id, party_id, row["candidate"],
                 row["year"], row["votes"], row["total_valid_votes"]),
            )
    return get_import(store, project_id, import_id)


def list_imports(store: Store, project_id: str) -> list[dict]:
    store.project(project_id)
    with store._connect() as db:
        return [dict(r) for r in db.execute("""SELECT r.*,s.status AS source_status
            FROM election_result_imports r
            JOIN sources s ON s.id=r.source_id AND s.project_id=r.project_id
            WHERE r.project_id=? ORDER BY r.imported_at DESC,r.id DESC""", (project_id,))]


def get_import(store: Store, project_id: str, import_id: str) -> dict:
    store.project(project_id)
    store._check_id(import_id)
    with store._connect() as db:
        meta = db.execute("""SELECT r.*,s.status AS source_status,s.name AS source_name
            FROM election_result_imports r
            JOIN sources s ON s.id=r.source_id AND s.project_id=r.project_id
            WHERE r.project_id=? AND r.id=?""", (project_id, import_id)).fetchone()
        if meta is None:
            raise NotFound("Election results import not found in project")
        rows = [dict(r) for r in db.execute(
            """SELECT * FROM election_candidate_results WHERE import_id=? ORDER BY source_line""",
            (import_id,),
        )]
    return {"import": dict(meta), "rows": rows, "quality": _quality(rows)}
