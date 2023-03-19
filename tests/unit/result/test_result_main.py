from datetime import date
from unittest import mock

from lotto.account import Account
from lotto.lotto import Lotto
from lotto.secret import Secret
from lotto.types import DateRange, Table
from result.main import outputs, result, inputs


def test_inputs(monkeypatch):
    monkeypatch.setenv('LOTTERY_ACCOUNT_ID', '복권 계정 아이디')
    monkeypatch.setenv('LOTTERY_ACCOUNT_PASSWORD', '복권 계정 비밀번호')
    monkeypatch.setenv('SEARCH_START_DATE', '2022-12-31')
    monkeypatch.setenv('SEARCH_END_DATE', '2023-01-01')

    account, search_dates = inputs()

    assert account.id == '복권 계정 아이디'
    assert account.password == '복권 계정 비밀번호'
    assert search_dates.start == date(2022, 12, 31)
    assert search_dates.end == date(2023, 1, 1)


def test_optional_search_dates_default_is_today(monkeypatch):
    monkeypatch.setenv('LOTTERY_ACCOUNT_ID', '복권 계정 아이디')
    monkeypatch.setenv('LOTTERY_ACCOUNT_PASSWORD', '복권 계정 비밀번호')

    _, search_dates = inputs()

    assert search_dates.start == date.today()
    assert search_dates.end == date.today()


def test_outputs(github_output_contains):
    outputs(
        search_dates=DateRange(date(2020, 1, 1), date(2023, 12, 31)),
        table=Table(
            headers=['구입일자', '복권명', '회차', '선택번호/복권번호',
                     '구입매수', '당첨결과', '당첨금', '추첨일'],
            rows=[['2022-12-28', '로또6/45', '1071', '51738 ...',
                   '3', '미추첨', '-', '2023-01-01']],
        )
    )

    assert github_output_contains('start-date=2020-01-01')
    assert github_output_contains('end-date=2023-12-31')
    assert github_output_contains(
        "table={'"
        "headers': ['구입일자', '복권명', '회차', '선택번호/복권번호',"
        " '구입매수', '당첨결과', '당첨금', '추첨일'], "
        "'rows': [['2022-12-28', '로또6/45', '1071', '51738 ...',"
        " '3', '미추첨', '-', '2023-01-01']]}")
    assert github_output_contains(
        "summary=["
        "{'round': '1071회', 'draw_date': '2023-01-01',"
        " 'prize': '0원', 'quantity': '3장'}"
        "]"
    )


@mock.patch('result.main.outputs')
def test_result(mock_main_outputs):
    # given
    table = Table(headers=[], rows=[[]])
    account = Account('user-id', Secret('abcde!2@4%'))
    search_dates = DateRange(date(2022, 12, 31), date(2023, 1, 1))

    mock_lotto = mock.MagicMock(spec=Lotto)
    mock_lotto.login.return_value = None
    mock_lotto.result.return_value = table

    # when
    result(lotto=mock_lotto, account=account, search_dates=search_dates)

    # then
    mock_lotto.login.assert_called_once_with(account)
    mock_lotto.result.assert_called_once_with(search_dates)
    mock_main_outputs.assert_called_once_with(search_dates, table)
