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


def go_login() -> None:
    _driver.get(_login_url)


def login_input_boxs() -> List[WebElement]:
    assert _driver.current_url == _login_url
    return _driver.find_elements(By.CSS_SELECTOR, '#article .form input')


def login_button() -> WebElement:
    assert _driver.current_url == _login_url
    return _driver.find_element(By.CSS_SELECTOR, '#article .form a')


def go_lotto() -> None:
    _driver.get('https://ol.dhlottery.co.kr/olotto/game/game645.do')


# todo
def alert() -> Optional[Alert]:
    try:
        WebDriverWait(_driver, 5).until(expected_conditions.alert_is_present())
        return _driver.switch_to.alert
    except WebDriverException:
        return None


def layer_popup() -> WebElement:
    return _driver.find_element(By.CSS_SELECTOR, '#popupLayerAlert')


def amount_select() -> Select:
    return Select(_driver.find_element(By.CSS_SELECTOR, '#amoundApply'))


def auto_checkbox() -> WebElement:
    return _driver.find_element(By.CSS_SELECTOR, 'label[for="checkAutoSelect"]')


def apply_button() -> WebElement:
    return _driver.find_element(By.CSS_SELECTOR, '#btnSelectNum')


def buy_button() -> WebElement:
    return _driver.find_element(By.CSS_SELECTOR, '#btnBuy')


# todo
def confirm_button() -> WebElement:
    return _driver.find_element(By.CSS_SELECTOR, '#popupLayerConfirm input[value="확인"]')


def total_price() -> int:
    element = _driver.find_element(By.CSS_SELECTOR, '#payAmt')
    return int(element.text.replace(',', ''))


# todo
def title() -> str:
    return _driver.title


def go_my_buy(start_date: date, end_date: date) -> None:
    fmt = '%Y%m%d'  # YYYYMMDD
    _driver.get(f'{_base_url}/myPage.do?method=lottoBuyList'
                f'&searchStartDate={start_date.strftime(fmt)}'
                f'&searchEndDate={end_date.strftime(fmt)}'
                f'&lottoId=&nowPage=1')  # 로또 게임 아이디=LO40


def buy_results() -> List[dict[str, str]]:
    headers = [th.text for th in _driver.find_elements(By.CSS_SELECTOR, '.tbl_data thead th')]
    rows = _driver.find_elements(By.CSS_SELECTOR, '.tbl_data tbody tr')

    buys = []
    for row in rows:
        tds = row.find_elements(By.TAG_NAME, 'td')
        buys.append(dict(zip_longest(headers, [td.text for td in tds], fillvalue='')))

    return buys


def total_buy_result(buys: List[dict[str, str]]) -> dict[str, int]:
    amount = [extract_amount(lottery['당첨금']) for lottery in buys]
    count = [int(lottery['구입매수'] or 0) for lottery in buys]
    unpick = [int(lottery['구입매수'] or 0) for lottery in buys if lottery['당첨결과'] == '미추첨']

    return {
        '총 당첨금': sum(amount),
        '총 구입매수': sum(count),
        '미추첨': sum(unpick),
    }


def extract_amount(value: str) -> int:
    if not value or value == '-':
        return 0

    return int(''.join(filter(str.isdigit, value)))


# todo
def no_data_message() -> Optional[str]:
    """메세지 종류:
        로그인 후 이용이 가능합니다.
        조회 결과가 없습니다.
    """
    try:
        return _driver.find_element(By.CSS_SELECTOR, '.nodata').text
    except NoSuchElementException:
        return None
