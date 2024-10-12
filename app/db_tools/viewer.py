from typing import Tuple, List

from .base import BaseDB


class DBViewer(BaseDB):
    _GET_SCORES_TEMPLATE = "SELECT * FROM score_table ORDER BY -score LIMIT {count}"

    def get_ordered_scores(self, count: int = 5) -> List[Tuple[str, int]]:
        cur = self._conn.cursor()
        vals = cur.execute(self._GET_SCORES_TEMPLATE.format(count=count)).fetchall()
        cur.close()
        return vals
