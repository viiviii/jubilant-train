from lotto.account import Account


def test_account():
    account = Account('alice1032', 'apple1004!@')

    assert account.id == 'alice1032'
    assert account.password == 'apple1004!@'


def test_masked_password_when_display():
    account = Account('simsim2', 'banana1004')

    assert str(account) == 'id=simsim2, password=**********'
    assert repr(account) == 'Account(id=simsim2, password=**********)'
