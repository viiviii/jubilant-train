import pytest

from sends.auth import Auth


def _auth(token='zbc-bzA2p', owner='octocat', repository='octocat/Hello-World'):
    return Auth(token=token, owner=owner, repository=repository)


def test_auth():
    auth = _auth(token='Abc-Dz132', owner='squid', repository='squid/Hello-Earth')

    assert auth.token == 'Abc-Dz132'
    assert auth.owner == 'squid'
    assert auth.repository == 'squid/Hello-Earth'


def test_raise_when_token_empty():
    with pytest.raises(ValueError, match='인증 정보는 필수 값 입니다.'):
        _auth(token='')


def test_raise_when_owner_empty():
    with pytest.raises(ValueError, match='인증 정보는 필수 값 입니다.'):
        _auth(owner='')


def test_raise_when_repository_empty():
    with pytest.raises(ValueError, match='인증 정보는 필수 값 입니다.'):
        _auth(repository='')


def test_masked_token_when_display():
    auth = _auth(token='abc-M3z', owner='squid', repository='nana/examples')

    assert str(auth) == 'token=*******, owner=squid, repository=nana/examples'
    assert repr(auth) == 'Auth(token=*******, owner=squid, repository=nana/examples)'


def test_masked_token_when_raises():
    with pytest.raises(ValueError) as err:
        _auth(owner='', token='abc-de7f')
    assert 'abc-de7f' not in str(err.value)
