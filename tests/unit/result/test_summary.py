from dataclasses import asdict

import pytest

from lotto.types import Table
from result.summary import total_prize, total_quantity, unique, Summary


def test_summary_from_table():
    # @formatter:off
    table = Table(
        headers=['구입일자', '복권명', '회차', '선택번호/복권번호', '구입매수', '당첨결과', '당첨금', '추첨일'],  # noqa
        rows=[['2022-12-28', '로또6/45', '1071', '51738 ...', '1', '당첨', '5,000원', '2023-01-01'],  # noqa
              ['2022-12-28', '로또6/45', '1071', '11001 ...', '2', '당첨', '5,000원', '2023-01-01']],  # noqa
    )

    summary = Summary.from_table(table)

    assert summary.name == '로또6/45'
    assert summary.round == '1071회'
    assert summary.draw_date == '2023-01-01'
    assert summary.prize == '10,000원'
    assert summary.quantity == '3장'
    # @formatter:on


@pytest.mark.parametrize('length', [1, 2, 3])
def test_unique(length):
    actual = unique(['로또6/45'] * length)

    assert actual == '로또6/45'


def test_raise_when_not_unique():
    not_unique = ['2020-01-01', '2023-12-31']

    with pytest.raises(ValueError, match='직전 회차의 해당 값은 유일해야 한다'):
        unique(not_unique)


def test_total_quantity():
    quantities = ['0', '1', '10', '100']

    actual = total_quantity(quantities)

    assert actual == 111


def test_total_prize():
    prizes = ['-', '5,000원', '50,000원']

    actual = total_prize(prizes)

    assert actual == 55_000


def test_as_dict():
    summary = Summary(
        name='로또6/45', round='1071회', draw_date='2023-01-01',
        prize='5,000원', quantity='10장'
    )

    actual = asdict(summary)

    assert actual == {
        'name': '로또6/45', 'round': '1071회', 'draw_date': '2023-01-01',
        'prize': '5,000원', 'quantity': '10장',
    }
