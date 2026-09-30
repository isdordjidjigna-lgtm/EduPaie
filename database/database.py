"""Gestion de la connexion SQLite et des transactions."""
import sqlite3
from contextlib import contextmanager
from pathlib import Path


class Database:
    def __init__(self, path: str = "edupaie.db"):
        self.path = path
        self.conn = sqlite3.connect(path, isolation_level=None)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")

    def init_schema(self, schema_path: str = "database/schema.sql"):
        sql = Path(schema_path).read_text(encoding="utf-8")
        self.conn.executescript(sql)

    @contextmanager
    def transaction(self):
        self.conn.execute("BEGIN")
        try:
            yield self.conn
            self.conn.execute("COMMIT")
        except Exception:
            self.conn.execute("ROLLBACK")
            raise

    def close(self):
        self.conn.close()