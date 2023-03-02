from datetime import date, timedelta

from selenium import webdriver

from check_lotto_result import message
from check_lotto_result.summary import group_by_round
from lotto.account import Account, fetch_account
from lotto.lotto import Lotto
from lotto.lotto_site import LottoSite
from lotto.secret import Secret
from lotto.types import DateRange
from sends.send import Send, SendResult
from sends.send_github_issue import SendGithubIssue


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
        account=fetch_account(),
        lotto=LottoSite(driver=webdriver.Chrome()),
        send=SendGithubIssue(token=Secret('ghp_'), repository='viiviii/jubilant-train'),  # todo: 하드코딩
        search_dates=DateRange(start=last_sunday(date.today()), end=date.today())
    )
