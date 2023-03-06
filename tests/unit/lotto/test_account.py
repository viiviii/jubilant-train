import pytest

from lotto.account import Account


def _account(id_='user-id', password='abcd1234!@'):
    return Account(id_=id_, password=password)


def test_account():
    account = _account('alice1032', 'apple1004!@')

    assert account.id == 'alice1032'
    assert account.password == 'apple1004!@'


def test_raise_when_id_empty():
    with pytest.raises(ValueError, match='계정 정보는 필수 값 입니다.'):
        _account(id_='')


def test_raise_when_password_empty():
    with pytest.raises(ValueError, match='계정 정보는 필수 값 입니다.'):
        _account(password='')


def test_masked_password_when_display():
    account = _account('simsim2', 'banana1004')

    assert str(account) == 'id=simsim2, password=**********'
    assert repr(account) == 'Account(id=simsim2, password=**********)'


def test_masked_password_when_raises():
    with pytest.raises(ValueError) as err:
        Account('', 'abcd1234!@')
    assert 'abcd1234!@' not in str(err.value)
