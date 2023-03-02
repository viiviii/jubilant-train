from typing import List

from selenium.webdriver.remote.webdriver import WebDriver

from lotto.account import Account
from lotto.lotto import Lotto
from lotto.site.pages import LoginPage, LottoPage, MyBuyPage
from lotto.types import DateRange


class Site(Lotto):

    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver

    def login(self, account: Account) -> None:
        page = LoginPage(driver=self._driver)

        page.go()
        page.login(account)

    def buy(self, amount: int) -> int:
        page = LottoPage(driver=self._driver)

        page.go()
        total_price = page.buy(amount)

        return total_price

    def result(self, dates: DateRange) -> List[dict[str, str]]:
        page = MyBuyPage(driver=self._driver)

        page.go(dates)
        buys = page.history()

        return buys.zip()
