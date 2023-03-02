from datetime import date
from textwrap import dedent
from typing import List

from check_lotto_result.check_latest_lotto_result import last_sunday, check_latest_lotto_result, DateRange
from lotto.lotto import Account
from lotto.lotto import Lotto
from sends.send import Send, SendResult


def test_last_sunday():
    sunday = date(2023, 1, 1)
    monday = date(2023, 1, 2)

    assert last_sunday(today=monday) == sunday
    assert last_sunday(today=sunday) == sunday


def test_check_latest_lotto_result():
    result = check_latest_lotto_result(
        account=Account(account_id='stub-id', account_password='stub-password'),
        lotto=StubLotto(),
        send=StubSend(),
        search_dates=DateRange(date(2023, 2, 12), date(2023, 2, 18))
    )

    assert result.title == '🎊 로또6/45 결과 (2023-02-12~2023-02-18)'
    assert result.content == dedent('''
        ### 1054회(2023-02-18)
        ```
        💰 당첨 금액: 0원
        🎯 구입 매수: 1장
        ```
        ''')


class StubLotto(Lotto):

    def login(self, account: Account) -> None:
        assert account.id == 'stub-id'
        assert account.password == 'stub-password'

    def buy(self, amount: int) -> int:
        pass

    def result(self, dates: DateRange) -> List[dict[str, str]]:
        assert dates == DateRange(date(2023, 2, 12), date(2023, 2, 18))
        return [{'구입일자': '2023-02-13', '복권명': '로또6/45', '회차': '1054',
                 '선택번호/복권번호': '51738 11491 27411 72232 76893 71219',
                 '구입매수': '1', '당첨결과': '미추첨', '당첨금': '-', '추첨일': '2023-02-18'}]


class StubSend(Send):
    def __call__(self, title: str, content: str) -> SendResult:
        return SendResult(title=title, content=content)
