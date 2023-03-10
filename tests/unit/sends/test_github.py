from sends.github import Github


def test_github():
    github = Github(token='Abc-Dz132', repository='squid/Hello-Earth')

    assert github.token == 'Abc-Dz132'
    assert github.repository == 'squid/Hello-Earth'


def test_masked_token_when_display():
    github = Github(token='abc-M3z', repository='nana/examples')

    assert str(github) == 'token=*******, repository=nana/examples'
    assert repr(github) == 'Github(token=*******, repository=nana/examples)'
