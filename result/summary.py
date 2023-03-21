from dataclasses import dataclass
from typing import List

from lotto.types import Table


@dataclass(frozen=True)
class Summary:
    name: str
    round: str
    draw_date: str
    prize: str
    quantity: str

    @classmethod
    def from_table(cls, table: Table):
        return cls(
            name=unique(table.values('복권명')),
            round=f"{unique(table.values('회차'))}회",
            draw_date=unique(table.values('추첨일')),
            quantity=f"{total_quantity(table.values('구입매수'))}장",
            prize=f"{total_prize(table.values('당첨금')):,}원",
        )


def unique(values: List[str]) -> str:
    value, *rest = set(values)
    if rest:
        raise ValueError('직전 회차의 해당 값은 유일해야 한다')
    return value


def total_quantity(quantities: List[str]) -> int:
    return sum(int(quantity) for quantity in quantities)


def total_prize(prize: List[str]) -> int:
    return sum(int(''.join(filter(str.isdigit, p))) for p in prize if p != '-')
