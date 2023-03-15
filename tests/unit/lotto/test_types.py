from dataclasses import asdict
from typing import Optional, List

import pytest

from lotto.types import Table


class TestTable:

    @pytest.fixture
    def create_table(self):
        def builder(rows: List, headers: Optional[List] = None):
            return Table(headers=headers or ['이름', '나이'], rows=rows)

        return builder

    def test_zip(self, create_table):
        headers = ['이름', '나이']
        rows = [['박덕배', '22'], ['장평수', '7']]

        actual = create_table(headers=headers, rows=rows).zip()

        assert len(actual) == 2
        assert actual[0] == {'이름': '박덕배', '나이': '22'}
        assert actual[1] == {'이름': '장평수', '나이': '7'}

    def test_zip_when_empty_rows(self, create_table):
        empty_arr = []

        actual = create_table(rows=empty_arr).zip()

        assert actual == []

    def test_zip_when_nested_empty_rows(self, create_table):
        nested_empty_arr = [[]]

        actual = create_table(rows=nested_empty_arr).zip()

        assert len(actual) == 1
        assert actual[0] == {'이름': '', '나이': ''}

    def test_as_dict(self, create_table):
        table = create_table(
            headers=['이름', '나이'],
            rows=[['박덕배', '22'], ['장평수', '7']]
        )

        actual = asdict(table)

        assert actual == {'headers': ['이름', '나이'],
                          'rows': [['박덕배', '22'], ['장평수', '7']]}
