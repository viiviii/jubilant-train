from lotto.types import Table
from result import markdown


def test_markdown_from_table():
    table = Table(
        headers=['복권명', '당첨금'],
        rows=[['스피또', '100원'],
              ['스피또', '999원']],
    )

    actual = markdown.from_table(table)

    assert actual == (
        '복권명|당첨금\n'
        ':---:|:---:\n'
        '스피또|100원\n'
        '스피또|999원\n'
    )
