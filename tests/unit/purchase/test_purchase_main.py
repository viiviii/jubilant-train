from unittest import mock

from lotto.account import Account
from lotto.lotto import Lotto
from lotto.secret import Secret
from purchase import main
from purchase.main import inputs


def test_inputs(monkeypatch):
    monkeypatch.setenv('LOTTERY_ACCOUNT_ID', '복권 계정 아이디')
    monkeypatch.setenv('LOTTERY_ACCOUNT_PASSWORD', '복권 계정 비밀번호')
    monkeypatch.setenv('LOTTERY_AMOUNT', '2')

    account, amount = inputs()

    assert account.id == '복권 계정 아이디'
    assert account.password == '복권 계정 비밀번호'
    assert amount == 2


def test_outputs(assert_contains_github_output):
    main.outputs(total_price=3000)

    assert_contains_github_output(
        name="total-price",
        value="3,000원"
    )


@mock.patch('purchase.main.outputs')
def test_buy(mock_main_outputs):
    # given
    account = Account('user-id', Secret('abcde!2@4%'))

    mock_lotto = mock.MagicMock(spec=Lotto)
    mock_lotto.buy.return_value = 3000

    # when
    main.buy(lotto=mock_lotto, account=account, amount=3)

    # then
    mock_lotto.login.assert_called_once_with(account)
    mock_lotto.buy.assert_called_once_with(amount=3)

    mock_main_outputs.assert_called_once_with(total_price=3000)
