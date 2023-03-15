from selenium.webdriver.common.by import By

from lotto.site.elements import Selector


def test_selector():
    selector = Selector(value='#id .class', description='테스트 아이디')

    assert selector == {'by': By.CSS_SELECTOR, 'value': '#id .class'}
    assert selector.description == '테스트 아이디'
