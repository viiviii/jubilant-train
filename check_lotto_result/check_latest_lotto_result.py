from datetime import date, timedelta

from check_lotto_result import message
from check_lotto_result.summary import group_by_round
from lotto.account import Account, from_env as account_from_env
from lotto.lotto import Lotto
from lotto.site.drivers import headless_chrome
from lotto.site.site import Site
from lotto.types import DateRange
from sends.auth import from_env as auth_from_env
from sends.github import Issue as SendGithubIssue
from sends.send import Send, SendResult


def last_sunday(today: date) -> date:
    days_in_week = 7
    pass_days_in_last_week = len(['일요일'])
    pass_days = (today.weekday() + pass_days_in_last_week) % days_in_week

    return today - timedelta(days=pass_days)


def check_latest_lotto_result(account: Account, lotto: Lotto, send: Send, search_dates: DateRange) -> SendResult:
    lotto.login(account)
    buys = lotto.result(search_dates)

    return send(title=message.title(search_dates),
                content=message.content(group_by_round(buys)))


if __name__ == '__main__':
    check_latest_lotto_result(
        account=account_from_env(),
        lotto=Site(driver=headless_chrome()),
        send=SendGithubIssue(auth=auth_from_env()),
        search_dates=DateRange(start=last_sunday(date.today()), end=date.today())
    )
