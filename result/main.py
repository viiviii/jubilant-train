import os
from dataclasses import asdict
from datetime import datetime, date
from typing import Optional, List

from lotto.account import Account
from lotto.lotto import Lotto
from lotto.site.drivers import headless_chrome
from lotto.site.site import Site
from lotto.types import DateRange
from result.summary import Summary, group_by_round


class Inputs:
    ID = 'LOTTERY_ACCOUNT_ID'
    PASSWORD = 'LOTTERY_ACCOUNT_PASSWORD'
    START_DATE = 'SEARCH_START_DATE'
    END_DATE = 'SEARCH_END_DATE'

    @staticmethod
    def to_account():
        return Account(
            id_=os.environ[Inputs.ID],
            password=os.environ[Inputs.PASSWORD],
        )

    @staticmethod
    def to_search_dates():
        def to_date(string: Optional[str]):
            if string:
                return datetime.strptime(string, '%Y-%m-%d').date()
            else:
                return date.today()

        return DateRange(
            start=to_date(os.getenv(Inputs.START_DATE)),
            end=to_date(os.getenv(Inputs.END_DATE))
        )


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
        summaries=group_by_round(buys),
    )


if __name__ == '__main__':
    result(
        lotto=Site(driver=headless_chrome()),
        account=Inputs.to_account(),
        search_dates=Inputs.to_search_dates()
    )
