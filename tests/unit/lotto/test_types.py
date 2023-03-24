from dataclasses import asdict
from datetime import date
from typing import Optional, List

import pytest

from lotto.types import Table, DateRange


class TestDateRange:

    def test_as_dict(self):
        dates = DateRange(start=date(2020, 1, 1), end=date(2023, 12, 31))

        actual = dates.as_dict()

        assert actual == {'start': '2020-01-01', 'end': '2023-12-31'}


class TestTable:

    @pytest.fixture
    def create_table(self):
        def builder(rows: List, headers: Optional[List] = None):
            return Table(headers=headers or ['이름', '나이'], rows=rows)

        return builder

    def test_values(self, create_table):
        table = create_table(
            headers=['이름', '나이'],
            rows=[['박덕배', '22'], ['장평수', '7']]
        )

        actual = table.values('이름')

        assert actual == ['박덕배', '장평수']

    def test_as_dict(self, create_table):
        table = create_table(
            headers=['이름', '나이'],
            rows=[['박덕배', '22'], ['장평수', '7']]
        )

        actual = asdict(table)

        assert actual == {
            'headers': ['이름', '나이'],
            'rows': [['박덕배', '22'], ['장평수', '7']]
        }
