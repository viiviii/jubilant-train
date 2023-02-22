from datetime import date, timedelta
from textwrap import dedent
from typing import NamedTuple

from lotto.account import Account, fetch_account
from lotto.lotto import Lotto
from lotto.lotto_site import LottoSite
from lotto.secret import Secret
from sends.send import Send, SendResult
from sends.send_github_issue import SendGithubIssue

DateRange = NamedTuple('DateRange', [('start', date), ('end', date)])


def last_sunday(today: date) -> date:
    days_in_week = 7
    pass_days_in_last_week = len(['일요일'])
    pass_days = (today.weekday() + pass_days_in_last_week) % days_in_week

    return today - timedelta(days=pass_days)


def to_title(name: str, rounds: str, draw_date: date):
    return f'🎊 {name} {rounds}회({draw_date.isoformat()})'


def to_content(total_amount: int, search_dates: DateRange) -> str:
    return dedent(f'''\
    💰 총 당첨금: {"{:,}".format(total_amount)}원
    📅 조회기간: {search_dates.start.strftime("%y-%m-%d")} ~ {search_dates.end.strftime("%y-%m-%d")}''')


def check_latest_lotto_result(account: Account, lotto: Lotto, send: Send, search_dates: DateRange) -> SendResult:
    lotto.login(account)
    buys = lotto.result(*search_dates)
    return send(title=to_title(name=buys['복권명'], rounds=buys['회차'], draw_date=buys['추첨일']),  # todo: title 하드 코딩 제거
                content=to_content(
                    total_amount=buys['총 당첨금'],
                    search_dates=DateRange(buys['조회 시작일'], buys['조회 종료일'])))


if __name__ == '__main__':
    check_latest_lotto_result(
        account=fetch_account(),
        lotto=LottoSite(),
        send=SendGithubIssue(token=Secret('ghp_'), repository='viiviii/jubilant-train'),  # todo: 하드코딩
        search_dates=(last_sunday(date.today()), date.today())  # todo: 일요일~토요일로 변경하기
    )
