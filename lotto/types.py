from dataclasses import dataclass
from datetime import date
from typing import List, NamedTuple


class DateRange(NamedTuple):
    start: date
    end: date

    def as_dict(self) -> dict:
        return {k: v.isoformat() for k, v in self._asdict().items()}


@dataclass(frozen=True)
class Table:
    headers: List[str]
    rows: List[List[str]]

    def values(self, key: str) -> List[str]:
        return [row[self.headers.index(key)] for row in self.rows]
