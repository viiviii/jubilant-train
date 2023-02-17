import pytest

from lotto.secret import Secret


@pytest.mark.parametrize(
    'original, expected',
    [(None, None), ('', ''), ('abc', 'abc')]
)
def test_value(original, expected):
    assert Secret(original).value == expected


@pytest.mark.parametrize(
    'original, expected',
    [(None, ''), ('', ''), ('abc', '***')]
)
def test_str(original, expected):
    assert str(Secret(original)) == expected


def test_repr():
    assert '***********' in repr(Secret('my-password'))
    assert 'my-password' not in repr(Secret('my-password'))


def test_eq():
    assert Secret('secret1234') == 'secret1234'
