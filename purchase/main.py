import os

import env
from lotto.account import Account
from lotto.lotto import Lotto
from lotto.site.drivers import headless_chrome
from lotto.site.site import Site


def inputs():
    return env.to_account(), int(os.getenv("LOTTERY_AMOUNT") or "1")


def outputs(total_price: int) -> None:
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print(f'total-price={"{:,.0f}원".format(total_price)}', file=fh)


def buy(lotto: Lotto, account: Account, amount: int) -> None:
    lotto.login(account)
    result = lotto.buy(amount=amount)

    outputs(total_price=result)


if __name__ == '__main__':
    buy(Site(headless_chrome()), *inputs())
