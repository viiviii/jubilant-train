from dataclasses import dataclass
from datetime import date
from itertools import zip_longest
from typing import NamedTuple, List

DateRange = NamedTuple('DateRange', [('start', date), ('end', date)])


@dataclass(frozen=True)
class Table:
    headers: List[str]
    rows: List[List[str]]

    def zip(self):
        return [dict(zip_longest(self.headers, cells, fillvalue=''))
                for cells in self.rows]
