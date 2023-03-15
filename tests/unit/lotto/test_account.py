from lotto.account import Account
from lotto.secret import Secret


def test_account():
    account = Account('alice1032', Secret('apple1004!@'))

    assert account.id == 'alice1032'
    assert account.password == 'apple1004!@'


def test_masked_password_when_display():
    account = Account('simsim2', Secret('banana1004'))

    assert 'banana1004' not in str(account)
    assert 'banana1004' not in repr(account)
