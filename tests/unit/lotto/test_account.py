import pytest

from lotto.account import Account


def test_account():
    account = Account('user-id', 'abcd1234!@')

    assert account.id == 'user-id'
    assert account.password == 'abcd1234!@'


def test_raise_when_when_id_empty():
    with pytest.raises(ValueError, match='아이디와 비밀번호는 필수 값이다'):
        Account('', 'abcd1234!@')


def test_raise_when_when_password_empty():
    with pytest.raises(ValueError, match='아이디와 비밀번호는 필수 값이다'):
        Account('user-id', '')


def test_masked_password_when_display():
    account = Account('user-id', 'abcd1234!@')

    assert str(account) == 'id=user-id, password=**********'
    assert repr(account) == 'Account(id=user-id, password=**********)'


def test_masked_password_when_raises():
    with pytest.raises(ValueError) as err:
        Account('', 'abcd1234!@')
    assert 'abcd1234!@' not in str(err.value)
