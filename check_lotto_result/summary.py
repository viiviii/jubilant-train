from dataclasses import dataclass
from itertools import groupby
from typing import List


@dataclass(frozen=True)
class Summary:
    """
    round  회차
    draw_date 추첨일
    prize 당첨금액
    quantity 구입매수
    """
    round: str
    draw_date: str
    prize: int
    quantity: int


def group_by_round(lotto_buys: List[dict[str, str]]) -> List[Summary]:
    grouped = []

    for _round, lotto_by_round in groupby(lotto_buys, key=lambda x: x['회차']):
        buys = list(lotto_by_round)

        grouped.append(Summary(
            round=_round,
            draw_date=buys[0]['추첨일'],
            quantity=sum([int(buy['구입매수']) for buy in buys]),
            prize=sum([prize_to_int(buy['당첨금']) for buy in buys])
        ))

    return grouped


def prize_to_int(value: str) -> int:
    if not value or value == '-':
        return 0

    return int(''.join(filter(str.isdigit, value)))
