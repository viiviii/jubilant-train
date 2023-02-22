from datetime import date
from itertools import zip_longest
from typing import List, Optional

from selenium import webdriver
from selenium.common import WebDriverException, NoSuchElementException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

_driver = webdriver.Chrome()

# todo
_base_url = 'https://dhlottery.co.kr'
_login_url = f'{_base_url}/user.do?method=login'


# todo
def alert() -> Optional[Alert]:
    try:
        WebDriverWait(_driver, 5).until(expected_conditions.alert_is_present())
        return _driver.switch_to.alert
    except WebDriverException:
        return None


# todo
def title() -> str:
    return _driver.title


class LoginPage:

    def go_login(self) -> None:
        _driver.get(_login_url)

    def login_input_boxs(self) -> List[WebElement]:
        assert _driver.current_url == _login_url
        return _driver.find_elements(By.CSS_SELECTOR, '#article .form input')

    def login_button(self) -> WebElement:
        assert _driver.current_url == _login_url
        return _driver.find_element(By.CSS_SELECTOR, '#article .form a')


class LottoPage:
    def go_lotto(self) -> None:
        _driver.get('https://ol.dhlottery.co.kr/olotto/game/game645.do')

    def auto_checkbox(self) -> WebElement:
        return _driver.find_element(By.CSS_SELECTOR, 'label[for="checkAutoSelect"]')

    def amount_select(self) -> Select:
        return Select(_driver.find_element(By.CSS_SELECTOR, '#amoundApply'))

    def apply_button(self) -> WebElement:
        return _driver.find_element(By.CSS_SELECTOR, '#btnSelectNum')

    def buy_button(self) -> WebElement:
        return _driver.find_element(By.CSS_SELECTOR, '#btnBuy')

    # todo
    def confirm_button(self) -> WebElement:
        return _driver.find_element(By.CSS_SELECTOR, '#popupLayerConfirm input[value="확인"]')

    def layer_popup(self) -> WebElement:
        return _driver.find_element(By.CSS_SELECTOR, '#popupLayerAlert')

    def total_price(self) -> int:
        element = _driver.find_element(By.CSS_SELECTOR, '#payAmt')
        return int(element.text.replace(',', ''))


class MyBuyPage:

    def go_my_buy(self, start_date: date, end_date: date) -> None:
        fmt = '%Y%m%d'  # YYYYMMDD
        _driver.get(f'{_base_url}/myPage.do?method=lottoBuyList'
                    f'&searchStartDate={start_date.strftime(fmt)}'
                    f'&searchEndDate={end_date.strftime(fmt)}'
                    f'&lottoId=&nowPage=1')  # 로또 게임 아이디=LO40

    # todo: 이 부분이 자꾸 이상한게 갑자기 여기만 객체처럼 메세지를 보내서임
    def buy_results(self) -> List[dict[str, str]]:
        headers = [th.text for th in _driver.find_elements(By.CSS_SELECTOR, '.tbl_data thead th')]
        rows = _driver.find_elements(By.CSS_SELECTOR, '.tbl_data tbody tr')

        buys = []
        for row in rows:
            tds = row.find_elements(By.TAG_NAME, 'td')
            buys.append(dict(zip_longest(headers, [td.text for td in tds], fillvalue='')))

        return buys

    def total_buy_result(self, buys: List[dict[str, str]]) -> dict[str, int]:
        amount = [self.extract_amount(lottery['당첨금']) for lottery in buys]
        count = [int(lottery['구입매수'] or 0) for lottery in buys]
        unpick = [int(lottery['구입매수'] or 0) for lottery in buys if lottery['당첨결과'] == '미추첨']

        return {
            '총 당첨금': sum(amount),
            '총 구입매수': sum(count),
            '미추첨': sum(unpick),
        }

    def extract_amount(self, value: str) -> int:
        if not value or value == '-':
            return 0

        return int(''.join(filter(str.isdigit, value)))

    # todo
    def no_data_message(self) -> Optional[str]:
        """메세지 종류:
            로그인 후 이용이 가능합니다.
            조회 결과가 없습니다.
        """
        try:
            return _driver.find_element(By.CSS_SELECTOR, '.nodata').text
        except NoSuchElementException:
            return None
