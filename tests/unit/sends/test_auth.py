from sends.auth import Auth


def test_auth():
    auth = Auth(token='Abc-Dz132', owner='squid', repository='squid/Hello-Earth')

    assert auth.token == 'Abc-Dz132'
    assert auth.owner == 'squid'
    assert auth.repository == 'squid/Hello-Earth'


def test_masked_token_when_display():
    auth = Auth(token='abc-M3z', owner='squid', repository='nana/examples')

    assert str(auth) == 'token=*******, owner=squid, repository=nana/examples'
    assert repr(auth) == 'Auth(token=*******, owner=squid, repository=nana/examples)'
