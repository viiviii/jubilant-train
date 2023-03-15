import os
from dataclasses import asdict
from typing import List

import env
from lotto.account import Account
from lotto.lotto import Lotto
from lotto.site.drivers import headless_chrome
from lotto.site.site import Site
from lotto.types import DateRange
from result.summary import Summary, group_by_round


def inputs():
    return env.to_account(), env.to_search_date_range()


def outputs(search_dates: DateRange, summaries: List[Summary]):
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print(f'start-date={search_dates.start}', file=fh)
        print(f'end-date={search_dates.end}', file=fh)
        print(f'summary={[asdict(s) for s in summaries]}', file=fh)


def result(lotto: Lotto, account: Account, search_dates: DateRange):
    lotto.login(account)
    buys = lotto.result(search_dates)
    outputs(
        search_dates=search_dates,
        summaries=group_by_round(buys.zip()),
    )


if __name__ == '__main__':
    result(Site(headless_chrome()), *inputs())
