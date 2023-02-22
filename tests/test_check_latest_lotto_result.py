from datetime import date
from typing import Any

from check_latest_lotto_result import to_content, last_sunday, check_latest_lotto_result, DateRange, to_title
from lotto.account import Account
from main import Lotto
from sends.send import Send, SendResult


def test_check_latest_lotto_result():
    result = check_latest_lotto_result(
        account=Account(account_id='id', account_password='password'),
        lotto=StubLotto(),
        send=StubSend(),
        search_dates=DateRange(date(2023, 2, 12), date(2023, 2, 18))
    )

    assert result.title == '🎊 로또6/45 1054회(2023-02-11)'
    assert result.content == ('💰 총 당첨금: 1,234,567원\n'
                              '📅 조회기간: 23-02-12 ~ 23-02-18')


class StubLotto(Lotto):

    def login(self, account: Account) -> None:
        pass

    def buy(self, amount: int) -> int:
        return amount * 1000

    def result(self, start: date, end: date) -> dict[str, Any]:
        return {'복권명': '로또6/45', '회차': 1054, '추첨일': date(2023, 2, 11),
                '총 당첨금': 1234567,
                '조회 시작일': start, '조회 종료일': end}


class StubSend(Send):
    def __call__(self, title: str, content: str) -> SendResult:
        return SendResult(title=title, content=content)


def test_last_sunday():
    sunday = date(2023, 1, 1)
    monday = date(2023, 1, 2)

    assert last_sunday(today=monday) == sunday
    assert last_sunday(today=sunday) == sunday


def test_to_title():
    actual = to_title(name='로또6/45', rounds='1054', draw_date=date(2023, 2, 11))

    assert actual == '🎊 로또6/45 1054회(2023-02-11)'


def test_to_content():
    actual = to_content(
        total_amount=0,
        search_dates=DateRange(date(2020, 1, 1), date(2021, 11, 28)))

    assert actual == (
        '💰 총 당첨금: 0원\n'
        '📅 조회기간: 20-01-01 ~ 21-11-28')
