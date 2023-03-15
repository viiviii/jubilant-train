from textwrap import dedent
from typing import List

from lotto.types import DateRange
from result.summary import Summary


def title(search_dates: DateRange):
    yyyymmdd = '%Y-%m-%d'
    return f'🎊 로또6/45 결과 ({search_dates.start.strftime(yyyymmdd)}~{search_dates.end.strftime(yyyymmdd)})'


def content(summaries: List[Summary]) -> str:
    return ''.join([_summary(lotto) for lotto in summaries])


def _summary(lotto: Summary) -> str:
    return dedent(f'''
        ### {lotto.round}회({lotto.draw_date})
        ```
        💰 당첨 금액: {"{:,}".format(lotto.prize)}원
        🎯 구입 매수: {lotto.quantity}장
        ```
        ''')
