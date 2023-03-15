from dataclasses import dataclass
from itertools import groupby
from typing import List, Iterable


@dataclass(frozen=True)
class Summary:
    """
    round  회차
    draw_date 추첨일
    prize 총 당첨금액
    quantity 총 구입매수
    """
    round: str
    draw_date: str
    prize: str
    quantity: str


def group_by_round(lotto_buys: List[dict[str, str]]) -> List[Summary]:
    grouped = []

    for _round, lotto_by_round in groupby(lotto_buys, key=lambda x: x['회차']):
        buys = list(lotto_by_round)

        grouped.append(Summary(
            round=f'{_round}회',
            draw_date=buys[0]['추첨일'],
            quantity=total_quantity(buy['구입매수'] for buy in buys),
            prize=total_prize(buy['당첨금'] for buy in buys)
        ))

    return grouped


def total_quantity(quantities: Iterable[str]) -> str:
    return f'{sum(int(quantity) for quantity in quantities)}장'


def total_prize(prizes: Iterable[str]) -> str:
    total = sum(
        int(''.join(filter(str.isdigit, p))) for p in prizes if p != '-'
    )

    return f'{total:,}원'
