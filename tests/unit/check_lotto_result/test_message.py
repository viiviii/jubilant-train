from datetime import date
from textwrap import dedent

from check_lotto_result.message import title, content
from check_lotto_result.summary import Summary
from lotto.types import DateRange


def test_title():
    dates = DateRange(date(2023, 1, 1), date(2023, 12, 31))

    actual = title(search_dates=dates)

    assert actual == 'π λ‘λ6/45 κ²°κ³Ό (2023-01-01~2023-12-31)'


def test_content():
    summaries = [
        Summary(
            round='1054', draw_date='2023-02-11',
            prize=1234567890,
            quantity=1000
        ),
        Summary(
            round='1053', draw_date='2023-02-07',
            prize=0,
            quantity=1
        ),
    ]

    actual = content(summaries)

    assert actual == dedent('''
        ### 1054ν(2023-02-11)
        ```
        π° λΉμ²¨ κΈμ‘: 1,234,567,890μ
        π― κ΅¬μ λ§€μ: 1000μ₯
        ```
        
        ### 1053ν(2023-02-07)
        ```
        π° λΉμ²¨ κΈμ‘: 0μ
        π― κ΅¬μ λ§€μ: 1μ₯
        ```
        ''')
