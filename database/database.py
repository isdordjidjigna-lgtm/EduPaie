"""Gestion de la connexion SQLite et des transactions."""
import os
import sys
import sqlite3
from contextlib import contextmanager
from pathlib import Path


def get_base_dir():
    """Retourne le dossier de base (source OU .exe)."""
    if getattr(sys, 'frozen', False):
        # Mode .exe : les fichiers sont à côté de l'exécutable
        return os.path.dirname(sys.executable)
    else:
        # Mode source : la racine du projet
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_resource_path(relative_path):
    """Retourne le chemin d'une ressource (fonctionne en .exe et en source)."""
    if getattr(sys, 'frozen', False):
        # Mode .exe : les ressources sont extraites dans _MEIPASS
        base = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    else:
        # Mode source : à la racine du projet
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_path)


class Database:
    def __init__(self, path: str = None):
        if path is None:
            # La base est stockée à côté de l'exécutable (ou à la racine du projet)
            path = os.path.join(get_base_dir(), "edupaie.db")
        self.path = path
        self.conn = sqlite3.connect(path, isolation_level=None)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")

    def init_schema(self, schema_path: str = None):
        if schema_path is None:
            schema_path = get_resource_path("database/schema.sql")
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