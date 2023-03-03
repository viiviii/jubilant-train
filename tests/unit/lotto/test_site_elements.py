from selenium.webdriver.common.by import By

from lotto.site.elements import Selector, zip_table


def test_selector():
    selector = Selector(value='#id .class', description='테스트 아이디')

    assert selector == {'by': By.CSS_SELECTOR, 'value': '#id .class'}
    assert selector.description == '테스트 아이디'


def test_zip_table():
    headers = ['이름', '나이']
    rows = [['박덕배', '22'], ['장평수', '7']]

    actual = zip_table(headers, rows)

    assert len(actual) == 2
    assert actual[0] == {'이름': '박덕배', '나이': '22'}
    assert actual[1] == {'이름': '장평수', '나이': '7'}


def test_zip_table_when_empty_rows():
    headers = ['이름', '나이']
    rows = []

    actual = zip_table(headers, rows)

    assert actual == []


def test_zip_table_when_nested_empty_rows():
    headers = ['이름', '나이']
    rows = [[]]

    actual = zip_table(headers, rows)

    assert len(actual) == 1
    assert actual[0] == {'이름': '', '나이': ''}
