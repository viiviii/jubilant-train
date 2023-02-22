from lotto.lotto import Account


def test_masked_password_when_account_is_print():
    account = Account('user-id', 'secret0000')
    assert 'secret0000' not in str(account)
    assert 'secret0000' not in repr(account)
