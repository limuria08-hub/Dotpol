"""Canonical local project, evidence and artifact store for Dotpol P1.

No external credentials or services. All source content is user-submitted text.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

MAX_SOURCE_BYTES = 1024 * 1024
MAX_TITLE = 180


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def identifier() -> str:
    return uuid.uuid4().hex


def valid_id(value: str) -> bool:
    return bool(re.fullmatch(r"[a-f0-9]{32}", value))


class NotFound(Exception):
    pass


class InvalidInput(Exception):
    pass


class Store:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path).expanduser().resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _connect(self):
        connection = sqlite3.connect(self.db_path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _init(self):
        with self._connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS projects (
                    id TEXT PRIMARY KEY, title TEXT NOT NULL, created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS sources (
                    id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                    name TEXT NOT NULL, kind TEXT NOT NULL, origin TEXT NOT NULL,
                    sha256 TEXT NOT NULL, content TEXT NOT NULL, imported_at TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','withdrawn'))
                );
                CREATE INDEX IF NOT EXISTS idx_sources_project ON sources(project_id);
                CREATE TABLE IF NOT EXISTS artifacts (
                    id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                    question TEXT NOT NULL, answer TEXT NOT NULL, evidence_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
            """)

    def create_project(self, title: str) -> dict:
        title = title.strip()
        if not 1 <= len(title) <= MAX_TITLE:
            raise InvalidInput('Project title must be 1–180 characters')
        project = {'id': identifier(), 'title': title, 'created_at': now()}
        with self._connect() as db:
            db.execute('INSERT INTO projects VALUES (:id,:title,:created_at)', project)
        return project

    def projects(self) -> list[dict]:
        with self._connect() as db:
            return [dict(row) for row in db.execute('SELECT * FROM projects ORDER BY created_at DESC')]

    def project(self, project_id: str) -> dict:
        self._check_id(project_id)
        with self._connect() as db:
            row = db.execute('SELECT * FROM projects WHERE id=?', (project_id,)).fetchone()
        if row is None:
            raise NotFound('Project not found')
        return dict(row)

    @staticmethod
    def _check_id(value: str):
        if not valid_id(value):
            raise InvalidInput('Invalid identifier')

    def import_source(self, project_id: str, name: str, kind: str, content: str, origin: str = 'user-upload') -> dict:
        self.project(project_id)
        name = name.strip()
        if not name or len(name) > MAX_TITLE:
            raise InvalidInput('Source name must be 1–180 characters')
        if kind not in {'txt', 'csv', 'json'}:
            raise InvalidInput('Accepted formats: txt, csv, json')
        if not isinstance(content, str) or not content.strip() or len(content.encode('utf-8')) > MAX_SOURCE_BYTES:
            raise InvalidInput('Source must contain at most 1 MiB of nonempty UTF-8 text')
        if origin not in {'user-upload', 'synthetic-demo'}:
            raise InvalidInput('Source origin must be user-upload or synthetic-demo')
        if kind == 'json':
            try:
                json.loads(content)
            except (ValueError, TypeError) as exc:
                raise InvalidInput('JSON source is malformed') from exc
        if kind == 'csv':
            try:
                parsed = list(csv.reader(io.StringIO(content), strict=True))
                if not parsed or not any(cell.strip() for row in parsed for cell in row):
                    raise ValueError('CSV is empty')
            except (csv.Error, ValueError) as exc:
                raise InvalidInput('CSV source is malformed') from exc
        row = {
            'id': identifier(), 'project_id': project_id, 'name': name, 'kind': kind,
            'origin': origin, 'sha256': hashlib.sha256(content.encode('utf-8')).hexdigest(),
            'content': content, 'imported_at': now(), 'status': 'active'
        }
        with self._connect() as db:
            db.execute('''INSERT INTO sources
                (id,project_id,name,kind,origin,sha256,content,imported_at,status)
                VALUES (:id,:project_id,:name,:kind,:origin,:sha256,:content,:imported_at,:status)''', row)
        return {k:v for k,v in row.items() if k!='content'}

    def sources(self, project_id: str) -> list[dict]:
        self.project(project_id)
        with self._connect() as db:
            return [{k:v for k,v in dict(row).items() if k != 'content'} for row in db.execute(
                'SELECT * FROM sources WHERE project_id=? ORDER BY imported_at DESC', (project_id,))]

    def source(self, project_id: str, source_id: str) -> dict:
        self.project(project_id)
        self._check_id(source_id)
        with self._connect() as db:
            row = db.execute('SELECT * FROM sources WHERE id=? AND project_id=?', (source_id, project_id)).fetchone()
        if row is None:
            raise NotFound('Source not found in project')
        return dict(row)

    def withdraw(self, project_id: str, source_id: str) -> dict:
        self.source(project_id, source_id)
        with self._connect() as db:
            db.execute("UPDATE sources SET status='withdrawn' WHERE id=? AND project_id=?", (source_id, project_id))
        return self.source(project_id, source_id)

    def save_artifact(self, project_id: str, question: str, answer: str, evidence: list[dict]) -> dict:
        self.project(project_id)
        if not question.strip() or len(question) > 2000 or len(answer) > 100000:
            raise InvalidInput('Artifact question or answer length is invalid')
        for ref in evidence:
            source = self.source(project_id, ref['source_id'])
            if source['status'] != 'active' or source['sha256'] != ref.get('sha256'):
                raise InvalidInput('Artifact contains invalid or withdrawn source evidence')
            lineno = ref.get('line')
            lines = source['content'].splitlines()
            if not isinstance(lineno, int) or isinstance(lineno, bool) or not (1 <= lineno <= len(lines)):
                raise InvalidInput('Artifact evidence line does not exist')
            if ref.get('excerpt') != lines[lineno-1]:
                raise InvalidInput('Artifact evidence does not match source content')
        row = {'id': identifier(), 'project_id': project_id, 'question': question,
               'answer': answer, 'evidence_json': json.dumps(evidence), 'created_at': now()}
        with self._connect() as db:
            db.execute('INSERT INTO artifacts VALUES (:id,:project_id,:question,:answer,:evidence_json,:created_at)', row)
        return self._artifact(row)

    @staticmethod
    def _artifact(row):
        out=dict(row)
        out['evidence']=json.loads(out.pop('evidence_json'))
        return out

    def artifacts(self, project_id: str) -> list[dict]:
        self.project(project_id)
        with self._connect() as db:
            return [self._artifact(row) for row in db.execute(
                'SELECT * FROM artifacts WHERE project_id=? ORDER BY created_at DESC', (project_id,))]

    def artifact(self, project_id: str, artifact_id: str) -> dict:
        self.project(project_id)
        self._check_id(artifact_id)
        with self._connect() as db:
            row=db.execute('SELECT * FROM artifacts WHERE id=? AND project_id=?', (artifact_id,project_id)).fetchone()
        if row is None:
            raise NotFound('Artifact not found')
        return self._artifact(row)
