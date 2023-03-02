from dataclasses import dataclass
from itertools import zip_longest
from typing import Optional, List

from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from lotto.account import Account
from lotto.lotto import LottoError
from lotto.types import DateRange


class Selector(dict):
    value: str
    description: str

    def __init__(self, value: str, description: str) -> None:
        super().__init__(by=By.CSS_SELECTOR, value=value)
        self.description = description


@dataclass(frozen=True)
class Table:
    headers: List[str]
    rows: List[List[str]]

    @staticmethod
    def from_element(table: WebElement):
        assert table.tag_name == 'table'
        headers = table.find_elements(**Table.By.HEADERS)
        rows = table.find_elements(**Table.By.ROWS)

        return Table(
            headers=[th.text for th in headers],
            rows=[[td.text for td in row.find_elements(**Table.By.CELLS)] for row in rows]
        )

    def zip(self) -> List[dict[str, str]]:
        return [dict(zip_longest(self.headers, cells, fillvalue='')) for cells in self.rows]

    class By:
        HEADERS = Selector(value='thead th', description='테이블 헤더')
        ROWS = Selector(value='tbody tr', description='테이블 로우')
        CELLS = Selector(value='td', description='테이블 셀')


class LoginPage:
    URL = 'https://dhlottery.co.kr/user.do?method=login'

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
        password.send_keys(account.password)

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
            WebDriverWait(self._driver, 5).until(expected_conditions.alert_is_present())
            return self._driver.switch_to.alert
        except WebDriverException:
            return None

    class By:
        ACCOUNT_INPUTS = Selector(value='#article .form input', description='계정 정보 입력 박스 목록')
        LOGIN_BUTTON = Selector(value='#article .form a', description='로그인 버튼')


class LottoPage:
    URL = 'https://ol.dhlottery.co.kr/olotto/game/game645.do'

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

    class By:
        AUTO_CHECKBOX = Selector(value='label[for="checkAutoSelect"]', description='자동선택 체크박스')
        QUANTITY_SELECT = Selector(value='#amoundApply', description='적용수량 옵션 선택')
        APPLY_BUTTON = Selector(value='#btnSelectNum', description='옵션 적용 버튼')
        BUY_BUTTON = Selector(value='#btnBuy', description='구매하기 버튼')
        BUY_CONFIRM_BUTTON = Selector(value='#popupLayerConfirm input[value="확인"]', description='구매 확정 버튼')
        TOTAL_PRICE = Selector(value='#payAmt', description='결제 금액')  # todo: 최종 구매 레이어에서 가져오기
        FAILURE = Selector(value='#popupLayerAlert', description='경고 팝업')


class MyBuyPage:
    URL = 'https://dhlottery.co.kr/myPage.do?method=lottoBuyList'

    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver

    def go(self, dates: DateRange) -> None:
        self._go_search(dates)

        if self._has_failure():
            raise LottoError(reason='당첨 조회 실패', detail=self._failure_message())

    def history(self) -> Table:
        table = self._driver.find_element(**self.By.HISTORY_TABLE)
        return Table.from_element(table)

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

    class By:
        HISTORY_TABLE = Selector(value='.tbl_data', description='당첨 결과 테이블')
        FAILURE = Selector(value='.nodata', description='결과 없음 메세지')
