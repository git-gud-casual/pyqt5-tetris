from .base import BaseDB


class DBDeleter(BaseDB):
    _DELETE_ALL = "DELETE FROM score_table"

    def delete_all(self):
        cur = self._conn.cursor()
        cur.execute(self._DELETE_ALL)
        self._conn.commit()
        cur.close()
