from typing import List, Optional

from selenium import webdriver
from selenium.common import WebDriverException
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
