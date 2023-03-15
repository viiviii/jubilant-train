from typing import Optional, List

from selenium.common import WebDriverException, NoSuchElementException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from lotto.lotto import Account, LottoError
from lotto.site.elements import Table, LoginPageElements, LottoPageElements, \
    MyBuyPageElements, zip_table
from lotto.types import DateRange


class LoginPage:
    URL = 'https://dhlottery.co.kr/user.do?method=login'
    By = LoginPageElements

    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver

    def go(self):
        self._driver.get(self.URL)

    def login(self, account: Account) -> None:
        self._input(account)
        self._submit()

    def _input(self, account: Account) -> None:
        _id, password = self._driver.find_elements(**self.By.ACCOUNT_INPUTS)

        _id.send_keys(account.id)
        password.send_keys(account.password.value)

    def _submit(self) -> None:
        login = self._driver.find_element(**self.By.LOGIN_BUTTON)

        login.click()

        if self._has_failure():
            raise LottoError(reason='로그인 실패', detail=self._failure_message())

    def _has_failure(self) -> bool:
        return bool(self._failure())

    def _failure_message(self) -> str:
        return self._failure().text

    def _failure(self) -> Optional[Alert]:
        try:
            WebDriverWait(self._driver, 5).until(
                expected_conditions.alert_is_present())
            return self._driver.switch_to.alert
        except WebDriverException:
            return None


class LottoPage:
    URL = 'https://ol.dhlottery.co.kr/olotto/game/game645.do'
    By = LottoPageElements

    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver

    def go(self) -> None:
        self._driver.get(self.URL)

        if self._has_failure():
            raise LottoError(reason='로또 구매 실패', detail=self._failure_message())

    def buy(self, amount: int) -> int:
        self._select(amount)
        self._buy()

        if self._has_failure():
            raise LottoError(reason='로또 구매 실패', detail=self._failure_message())

        return self._total_price()

    def _select(self, amount: int) -> None:
        auto = self._driver.find_element(**self.By.AUTO_CHECKBOX)
        quantity = self._driver.find_element(**self.By.QUANTITY_SELECT)
        apply = self._driver.find_element(**self.By.APPLY_BUTTON)

        auto.click()
        Select(quantity).select_by_value(str(amount))
        apply.click()

    def _buy(self) -> None:
        buy = self._driver.find_element(**self.By.BUY_BUTTON)
        confirm = self._driver.find_element(**self.By.BUY_CONFIRM_BUTTON)

        buy.click()
        confirm.click()

    def _total_price(self) -> int:
        total_price = self._driver.find_element(**self.By.TOTAL_PRICE)
        return int(total_price.text.replace(',', ''))

    def _has_failure(self) -> bool:
        return self._failure().is_displayed()

    def _failure_message(self) -> str:
        return self._failure().text

    def _failure(self) -> WebElement:
        return self._driver.find_element(**self.By.FAILURE)


class MyBuyPage:
    URL = 'https://dhlottery.co.kr/myPage.do?method=lottoBuyList'
    By = MyBuyPageElements

    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver

    def go(self, dates: DateRange) -> None:
        self._go_search(dates)

        if self._has_failure():
            raise LottoError(reason='당첨 조회 실패', detail=self._failure_message())

    def history(self) -> List[dict[str, str]]:
        table = Table(self._driver)
        return zip_table(header=table.headers_to_texts(),
                         rows=table.rows_to_texts())

    def _go_search(self, dates: DateRange) -> None:
        # todo: page 여러 개인 경우? nowPage 부분 수정
        start, end = [dt.strftime('%Y%m%d') for dt in dates]
        query = f'&searchStartDate={start}&searchEndDate={end}&lottoId=LO40&nowPage=1'

        self._driver.get(f'{self.URL}{query}')

    def _has_failure(self) -> bool:
        return bool(self._failure())

    def _failure_message(self) -> str:
        return self._failure().text

    def _failure(self) -> Optional[WebElement]:
        """
        로그인 후 이용이 가능합니다.
        조회 결과가 없습니다.
        """
        try:
            return self._driver.find_element(**self.By.FAILURE)
        except NoSuchElementException:
            return None
