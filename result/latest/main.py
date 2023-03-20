from datetime import date, timedelta

import env
from lotto.account import Account
from lotto.lotto import Lotto
from lotto.site.drivers import headless_chrome
from lotto.site.site import Site
from lotto.types import DateRange
from result.main import result


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


def latest_result(lotto: Lotto, account: Account) -> None:
    result(lotto=lotto, account=account, search_dates=latest())


if __name__ == '__main__':
    latest_result(Site(headless_chrome()), inputs())
