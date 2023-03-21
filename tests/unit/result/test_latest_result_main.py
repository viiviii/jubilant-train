from datetime import date
from unittest import mock

from lotto.account import Account
from lotto.lotto import Lotto
from lotto.secret import Secret
from lotto.types import DateRange, Table
from result.latest.main import latest_saturday, latest, inputs, latest_result, \
    outputs


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


def test_outputs(github_output_contains):
    # @formatter:off
    outputs(
        search_dates=DateRange(date(2020, 1, 1), date(2023, 12, 31)),
        table=Table(
            headers=['구입일자', '복권명', '회차', '선택번호/복권번호', '구입매수', '당첨결과', '당첨금', '추첨일'], # noqa
            rows=[['2022-12-28', '로또6/45', '1071', '51738 ...', '2', '미추첨', '-', '2023-01-01'], # noqa
                  ['2022-12-28', '로또6/45', '1071', '11001 ...', '3', '미추첨', '-', '2023-01-01']], # noqa
        )
    )

    assert github_output_contains('start-date=2020-01-01')
    assert github_output_contains('end-date=2023-12-31')
    assert github_output_contains(
        "summary={"
        "'name': '로또6/45', 'round': '1071회', 'draw_date': '2023-01-01', 'prize': '0원', 'quantity': '5장'" # noqa
        "}"
    )
    assert github_output_contains(
        "table={'"
        "headers': ["
        "'구입일자', '복권명', '회차', '선택번호/복권번호', '구입매수', '당첨결과', '당첨금', '추첨일'"
        "], "
        "'rows': ["
        "['2022-12-28', '로또6/45', '1071', '51738 ...', '2', '미추첨', '-', '2023-01-01'], " # noqa
        "['2022-12-28', '로또6/45', '1071', '11001 ...', '3', '미추첨', '-', '2023-01-01']" # noqa
        "]}"
    )
    # @formatter:on


@mock.patch('result.latest.main.outputs')
def test_result(mock_main_outputs):
    # given
    table = Table(headers=[], rows=[])
    account = Account('user-id', Secret('abcde!2@4%'))

    mock_lotto = mock.MagicMock(spec=Lotto)
    mock_lotto.result.return_value = table

    # when
    latest_result(lotto=mock_lotto, account=account)

    # then
    mock_lotto.login.assert_called_once_with(account)
    mock_lotto.result.assert_called_once_with(dates=latest())

    mock_main_outputs.assert_called_once_with(
        search_dates=latest(),
        table=table
    )
