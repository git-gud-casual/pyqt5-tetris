import sqlite3

from contextlib import suppress

from config import DATABASE_PATH


class BaseDB:
    _conn: sqlite3.Connection

    def __init__(self, database_path: str = DATABASE_PATH):
        self._conn = sqlite3.connect(database_path)

    def __del__(self):
        with suppress(Exception):
            self._conn.close()
