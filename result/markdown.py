from lotto.types import Table


def from_table(table: Table) -> str:
    headers = '|'.join(table.headers)
    separator = '|'.join([':---:' for _ in table.headers])
    rows = '\n'.join(['|'.join(row) for row in table.rows])
    return f'{headers}\n{separator}\n{rows}\n'
