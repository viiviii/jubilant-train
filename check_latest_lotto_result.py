from datetime import date, timedelta
from textwrap import dedent
from typing import Any

from lotto.account import Account, fetch_account
from lotto.secret import Secret
from main import login, check_lottery_result
from sends.send import Send, SendResult
from sends.send_github_issue import SendGithubIssue


def last_sunday(today: date) -> date:
    days_in_week = 7
    pass_days_in_last_week = len(['일요일'])
    pass_days = (today.weekday() + pass_days_in_last_week) % days_in_week

    return today - timedelta(days=pass_days)


def to_message(result: dict[str, Any]) -> str:
    return dedent(f'''\
    💰 총 당첨금: {"{:,}".format(result["총 당첨금"])}원
    ✅ 총 구입매수: {result["총 구입매수"]}장 (미추첨 {result["미추첨"]}장)
    📅 조회기간: {result["시작일"].strftime("%y-%m-%d")} ~ {result["종료일"].strftime("%y-%m-%d")}''')


def check_latest_lotto_result(account: Account, send: Send) -> SendResult:
    login(account)
    lottery_result = check_lottery_result(start_date=last_sunday(date.today()), end_date=date.today())
    return send(title='🎊 로또6/45 1055회(23-02-18)',  # todo: title 하드 코딩 제거
                content=to_message(lottery_result))


if __name__ == '__main__':
    check_latest_lotto_result(
        account=fetch_account(),
        send=SendGithubIssue(token=Secret('ghp_'), repository='viiviii/jubilant-train')  # todo: 하드코딩
    )
