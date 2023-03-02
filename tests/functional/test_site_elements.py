import pytest
from selenium.webdriver.common.by import By

from lotto.site.pages import LoginPage, LottoPage, MyBuyPage, Selector, Table


@pytest.fixture(scope='class')
def load(driver, page):
    driver.get(page.URL)


@pytest.fixture(scope='class')
def by(page):
    return page.By


@pytest.fixture(scope='class')
def find_element(driver):
    return lambda selector: driver.find_element(**selector)


@pytest.fixture(scope='class')
def find_elements(driver):
    return lambda selector: driver.find_elements(**selector)


@pytest.fixture(scope='class')
def login(driver, account):
    _page = LoginPage(driver)
    _page.go()
    _page.login(account)


class TestLoginPageElements:

    @pytest.fixture(scope='class')
    def page(self):
        return LoginPage

    @pytest.fixture(scope='class', autouse=True)
    def setup(self, load):
        pass

    def test_account_inputs(self, by, find_elements):
        elements = find_elements(by.ACCOUNT_INPUTS)

        assert len(elements) == 2
        assert elements[0].accessible_name == '아이디'
        assert elements[1].accessible_name == '비밀번호'

    def test_login_button(self, by, find_element):
        element = find_element(by.LOGIN_BUTTON)

        assert element
        assert element.accessible_name == '로그인'


class TestLottoPageElements:

    @pytest.fixture(scope='class')
    def page(self):
        return LottoPage

    @pytest.fixture(scope='class', autouse=True)
    def setup(self, login, load):
        pass

    def test_auto_checkbox(self, by, find_element):
        assert find_element(by.AUTO_CHECKBOX)

    def test_quantity_select(self, by, find_element):
        assert find_element(by.QUANTITY_SELECT)

    def test_apply_button(self, by, find_element):
        assert find_element(by.APPLY_BUTTON)

    def test_buy_button(self, by, find_element):
        assert find_element(by.BUY_BUTTON)

    def test_buy_confirm_button(self, by, find_element):
        assert find_element(by.BUY_CONFIRM_BUTTON)


class TestMyBuyPageElements:

    @pytest.fixture(scope='class')
    def page(self):
        return MyBuyPage

    @pytest.fixture(scope='class', autouse=True)
    def setup(self, login, load):
        pass

    def test_history_table(self, by, find_element):
        assert find_element(by.HISTORY_TABLE)

    def test_history_table_headers(self, by, find_element):
        headers = Table.from_element(find_element(by.HISTORY_TABLE)).headers
        assert '구입일자' in headers
        assert '복권명' in headers
        assert '회차' in headers
        assert '선택번호/복권번호' in headers
        assert '구입매수' in headers
        assert '당첨결과' in headers
        assert '당첨금' in headers
        assert '추첨일' in headers


def test_selector():
    selector = Selector(value='#id .class', description='테스트 아이디')

    assert selector == {'by': By.CSS_SELECTOR, 'value': '#id .class'}
    assert selector.description == '테스트 아이디'


def test_table_zip():
    table = Table(headers=['이름', '나이'], rows=[['박덕배', '22'], ['장평수', '7']])

    actual = table.zip()

    assert len(actual) == 2
    assert actual[0] == {'이름': '박덕배', '나이': '22'}
    assert actual[1] == {'이름': '장평수', '나이': '7'}


def test_table_zip_when_empty_rows():
    table = Table(headers=['이름', '나이'], rows=[])

    actual = table.zip()

    assert actual == []


def test_table_zip_when_nested_empty_rows():
    table = Table(headers=['이름', '나이'], rows=[[]])

    actual = table.zip()

    assert len(actual) == 1
    assert actual[0] == {'이름': '', '나이': ''}
