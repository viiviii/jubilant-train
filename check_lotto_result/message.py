from textwrap import dedent
from typing import List

from check_lotto_result.summary import Summary
from lotto.types import DateRange


def title(search_dates: DateRange):
    yyyymmdd = '%Y-%m-%d'
    return f'π λ‘λ6/45 κ²°κ³Ό ({search_dates.start.strftime(yyyymmdd)}~{search_dates.end.strftime(yyyymmdd)})'


def content(summaries: List[Summary]) -> str:
    return ''.join([_summary(lotto) for lotto in summaries])


def _summary(lotto: Summary) -> str:
    return dedent(f'''
        ### {lotto.round}ν({lotto.draw_date})
        ```
        π° λΉμ²¨ κΈμ‘: {"{:,}".format(lotto.prize)}μ
        π― κ΅¬μ λ§€μ: {lotto.quantity}μ₯
        ```
        ''')
