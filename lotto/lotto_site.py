from datetime import date
from typing import Any

from selenium.webdriver.remote.webdriver import WebDriver

from lotto.lotto import Account
from lotto.lotto import Lotto
from lotto.lotto_site_page import LoginPage, LottoPage, MyBuyPage


class LottoSite(Lotto):

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

    def result(self, start: date, end: date) -> dict[str, Any]:
        page = MyBuyPage(driver=self._driver)

        page.go()
        results = page.search(dates=(start, end))

        return {'조회 시작일': start, '조회 종료일': end} | page.total_buy_result(results)
