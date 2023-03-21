import os
from dataclasses import asdict
from datetime import date, timedelta

import env
from lotto.account import Account
from lotto.lotto import Lotto
from lotto.site.drivers import headless_chrome
from lotto.site.site import Site
from lotto.types import DateRange, Table
from result.summary import Summary


def latest_saturday(today: date) -> date:
    DAYS_IN_WEEK = 7

    pass_days_in_last_week = len(['일요일', '토요일'])
    pass_days = (today.weekday() + pass_days_in_last_week) % DAYS_IN_WEEK

    return today - timedelta(days=pass_days)


def latest() -> DateRange:
    SALES_DAYS = 7

    latest_draw_date = latest_saturday(date.today())
    sales_start_date = latest_draw_date - timedelta(days=SALES_DAYS - 1)

    return DateRange(start=sales_start_date, end=latest_draw_date)


def inputs():
    return env.to_account()


def outputs(search_dates: DateRange, table: Table) -> None:
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print(f'start-date={search_dates.start}', file=fh)
        print(f'end-date={search_dates.end}', file=fh)
        print(f'summary={asdict(Summary.from_table(table))}', file=fh)
        print(f'table={asdict(table)}', file=fh)


def latest_result(lotto: Lotto, account: Account) -> None:
    latest_dates = latest()

    lotto.login(account)
    buys = lotto.result(dates=latest_dates)

    outputs(search_dates=latest_dates, table=buys)


if __name__ == '__main__':
    latest_result(Site(headless_chrome()), inputs())
