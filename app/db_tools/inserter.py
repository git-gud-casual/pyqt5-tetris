from .base import BaseDB


class DBInserter(BaseDB):
    _ADD_SCORE_TEMPLATE = "INSERT INTO score_table(name, score) VALUES(?, ?)"

    def add_score(self, name: str, score: int):
        cur = self._conn.cursor()
        cur.execute(self._ADD_SCORE_TEMPLATE, (name, score))
        cur.close()
        self._conn.commit()
