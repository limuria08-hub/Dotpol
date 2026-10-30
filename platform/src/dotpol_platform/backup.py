"""P1.02 consistent local SQLite backups without a second data store.

No browser endpoint. SQLite backup snapshots WAL changes rather than copying
an active database file; the operator chooses the destination explicitly.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import sqlite3
from contextlib import closing
from pathlib import Path

from .store import Store, InvalidInput


def verify_backup(path: str | Path) -> bool:
    """Read-only integrity check; invalid snapshots must not be restored."""
    target = Path(path).expanduser().resolve()
    if not target.is_file():
        return False
    try:
        with closing(sqlite3.connect(f"file:{target.as_posix()}?mode=ro", uri=True)) as db:
            row = db.execute("PRAGMA integrity_check").fetchone()
            if not row or row[0] != 'ok':
                return False
            for table in ('projects', 'sources', 'artifacts'):
                if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)).fetchone():
                    return False
        return True
    except (OSError, sqlite3.DatabaseError):
        return False


def backup_store(store: Store, destination: str | Path) -> dict:
    """Atomic, non-overwriting, local operator-initiated backup."""
    target = Path(destination).expanduser().resolve()
    if target == store.db_path:
        raise InvalidInput('Backup destination cannot be the live database')
    if target.exists():
        raise InvalidInput('Backup destination already exists; choose a new filename')
    if not target.parent.is_dir():
        raise InvalidInput('Backup destination directory does not exist')
    tmp = target.with_name(target.name + '.pending')
    if tmp.exists():
        raise InvalidInput('Pending backup exists; inspect it before retrying')
    try:
        fd = os.open(tmp, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.close(fd)
        with closing(store._connect()) as original, closing(sqlite3.connect(tmp)) as snapshot:
            original.backup(snapshot)
        if not verify_backup(tmp):
            raise InvalidInput('Backup integrity check failed')
        os.chmod(tmp, 0o600)
        if target.exists():
            raise InvalidInput('Backup destination appeared during creation')
        os.replace(tmp, target)
        return {
            'destination': str(target),
            'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
            'verified': True, 'size_bytes': target.stat().st_size,
        }
    finally:
        if tmp.exists():
            tmp.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description='Back up the local Dotpol SQLite database')
    parser.add_argument('--output', required=True, help='New .sqlite3 destination, existing parent')
    args = parser.parse_args()
    db_path = Path(os.environ.get('DOTPOL_DATA_DIR', str(Path.home()/'.dotpol'))) / 'dotpol.sqlite3'
    if not db_path.is_file():
        parser.error('No existing local Dotpol database to back up')
    print(backup_store(Store(db_path), args.output))


if __name__ == '__main__':
    main()
