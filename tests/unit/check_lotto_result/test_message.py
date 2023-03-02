from datetime import date
from textwrap import dedent

from check_lotto_result.message import title, content
from check_lotto_result.summary import Summary
from lotto.types import DateRange


def test_title():
    dates = DateRange(date(2023, 1, 1), date(2023, 12, 31))

    actual = title(search_dates=dates)

    assert actual == '🎊 로또6/45 결과 (2023-01-01~2023-12-31)'


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
        ### 1054회(2023-02-11)
        ```
        💰 당첨 금액: 1,234,567,890원
        🎯 구입 매수: 1000장
        ```
        
        ### 1053회(2023-02-07)
        ```
        💰 당첨 금액: 0원
        🎯 구입 매수: 1장
        ```
        ''')
