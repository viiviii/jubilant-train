from datetime import date
from unittest import mock
from unittest.mock import ANY

from lotto.account import Account
from lotto.lotto import Lotto
from lotto.secret import Secret
from result.latest.main import latest_saturday, latest, inputs, latest_result


def test_latest_saturday():
    saturday = date(2022, 12, 31)
    monday = date(2023, 1, 2)

    assert latest_saturday(today=monday) == saturday
    assert latest_saturday(today=saturday) == saturday


def test_latest():
    SATURDAY = 5
    SUNDAY = 6

    sales_start_date, sales_end_date = latest()

    assert sales_start_date.weekday() == SUNDAY
    assert sales_end_date.weekday() == SATURDAY
    assert (sales_end_date - sales_start_date).days == 6


def test_inputs(monkeypatch):
    monkeypatch.setenv('LOTTERY_ACCOUNT_ID', '복권 계정 아이디')
    monkeypatch.setenv('LOTTERY_ACCOUNT_PASSWORD', '복권 계정 비밀번호')

    account = inputs()

    assert account.id == '복권 계정 아이디'
    assert account.password == '복권 계정 비밀번호'


@mock.patch('result.latest.main.result')
def test_result(mock_result):
    # given
    account = Account('user-id', Secret('abcde!2@4%'))
    search_dates_is_latest = latest()

    # when
    latest_result(lotto=mock.Mock(spec=Lotto), account=account)

    # then
    mock_result.assert_called_once_with(
        lotto=ANY,
        account=account,
        search_dates=search_dates_is_latest
    )
