from datetime import date
from unittest import mock

import pytest

from lotto.account import Account
from lotto.lotto import Lotto
from lotto.types import DateRange
from result.main import outputs, result, inputs
from result.summary import Summary


@pytest.fixture
def github_output(tmp_path, monkeypatch):
    path = tmp_path / "outputs.txt"
    monkeypatch.setenv('GITHUB_OUTPUT', str(path))

    return path


@pytest.fixture
def github_output_contains(github_output):
    def contains(expected):
        return f'{expected}\n' in github_output.read_text()

    return contains


def test_all_inputs(monkeypatch):
    monkeypatch.setenv('LOTTERY_ACCOUNT_ID', '복권 계정 아이디')
    monkeypatch.setenv('LOTTERY_ACCOUNT_PASSWORD', '복권 계정 비밀번호')
    monkeypatch.setenv('SEARCH_START_DATE', '2022-12-31')
    monkeypatch.setenv('SEARCH_END_DATE', '2023-01-01')

    account, search_dates = inputs()

    assert account.id == '복권 계정 아이디'
    assert account.password == '복권 계정 비밀번호'  # todo
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
        summaries=[
            Summary(round='9', draw_date='2023-01-01', prize=0, quantity=3)
        ],
    )

    assert github_output_contains('start-date=2020-01-01')
    assert github_output_contains('end-date=2023-12-31')
    assert github_output_contains(
        "summary=["
        "{'round': '9', 'draw_date': '2023-01-01', 'prize': 0, 'quantity': 3}"
        "]"
    )


def test_result(github_output_contains):
    # given
    mock_lotto = mock.MagicMock(spec=Lotto)
    mock_lotto.login.return_value = None
    mock_lotto.result.return_value = [
        {
            '구입일자': '2023-01-01', '복권명': '로또6/45', '회차': '3',
            '선택번호/복권번호': '51738 11491 27411 72232 76893 71219',
            '구입매수': '1', '당첨결과': '미추첨', '당첨금': '-', '추첨일': '2023-01-05'
        }
    ]

    account = Account('fake-user-id', 'abcde!2@4%')
    search_dates = DateRange(date(2022, 12, 31), date(2023, 1, 1))

    # when
    result(lotto=mock_lotto, account=account, search_dates=search_dates)

    # then
    mock_lotto.login.assert_called_once_with(account)
    mock_lotto.result.assert_called_once_with(search_dates)

    assert github_output_contains('start-date=2022-12-31')
    assert github_output_contains('end-date=2023-01-01')
    assert github_output_contains(
        "summary=["
        "{'round': '3', 'draw_date': '2023-01-05', 'prize': 0, 'quantity': 1}"
        "]"
    )
