from datetime import date
from itertools import zip_longest
from typing import List, Optional

from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from lotto.lotto import Account, LottoError


class Selector(dict):
    value: str
    description: str

    def __init__(self, value: str, description: str) -> None:
        super().__init__(by=By.CSS_SELECTOR, value=value)
        self.description = description


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

    def go(self) -> None:
        self._driver.get(self.URL)

        if self._has_failure():
            raise LottoError(reason='당첨 조회 실패', detail=self._failure_message())

    def search(self, dates: tuple[date, date]) -> List[dict[str, str]]:
        # todo: page 여러 개인 경우? nowPage 부분 수정
        start, end = [dt.strftime('%Y%m%d') for dt in dates]  # YYYYMMDD
        self._driver.get(f'{self.URL}&searchStartDate={start}&searchEndDate={end}&lottoId=LO40&nowPage=1')

        if self._has_failure():
            raise LottoError(reason='당첨 조회 실패', detail=self._failure_message())

        return self._buy_results()

    def _buy_results(self) -> List[dict[str, str]]:
        headers = [th.text for th in self._driver.find_elements(**self.By.TABLE_HEADER)]
        rows = self._driver.find_elements(**self.By.TABLE_ROW)

        buys = []
        for row in rows:
            tds = row.find_elements(By.TAG_NAME, 'td')
            buys.append(dict(zip_longest(headers, [td.text for td in tds], fillvalue='')))

        return buys

    # todo: 여기 맞냐
    def total_buy_result(self, buys: List[dict[str, str]]) -> dict[str, int]:
        amount = [self.extract_amount(lottery['당첨금']) for lottery in buys]
        count = [int(lottery['구입매수'] or 0) for lottery in buys]
        unpick = [int(lottery['구입매수'] or 0) for lottery in buys if lottery['당첨결과'] == '미추첨']

        return {
            '총 당첨금': sum(amount),
            '총 구입매수': sum(count),
            '미추첨': sum(unpick),
        }

    # todo: 여기 맞냐
    def extract_amount(self, value: str) -> int:
        if not value or value == '-':
            return 0

        return int(''.join(filter(str.isdigit, value)))

    def _has_failure(self) -> bool:
        return bool(self._failure())

    def _failure_message(self) -> str:
        return self._failure().text

    def _failure(self) -> Optional[WebElement]:
        """메세지 종류:
            로그인 후 이용이 가능합니다.
            조회 결과가 없습니다.
        """
        try:
            return self._driver.find_element(**self.By.FAILURE)
        except NoSuchElementException:
            return None

    class By:
        TABLE_HEADER = Selector(value='.tbl_data thead th', description='당첨 결과 테이블 헤더')
        TABLE_ROW = Selector(value='.tbl_data tbody tr', description='당첨 결과 테이블 로우')
        FAILURE = Selector(value='.nodata', description='결과 없음 메세지')
