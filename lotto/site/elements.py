from itertools import zip_longest
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class Selector(dict):
    value: str
    description: str

    def __init__(self, value: str, description: str) -> None:
        super().__init__(by=By.CSS_SELECTOR, value=value)
        self.description = description


class LoginPageElements:
    ACCOUNT_INPUTS = Selector(value='#article .form input',
                              description='계정 정보 입력 박스 목록')
    LOGIN_BUTTON = Selector(value='#article .form a', description='로그인 버튼')


# todo: TOTAL_PRICE 최종 구매 레이어에서 가져오기
# todo: 주간 구매한도(5천원) 예외 속성 추가하기 #recommend720Plus
class LottoPageElements:
    AUTO_CHECKBOX = Selector(value='label[for="checkAutoSelect"]',
                             description='자동선택 체크박스')
    QUANTITY_SELECT = Selector(value='#amoundApply', description='적용수량 옵션 선택')
    APPLY_BUTTON = Selector(value='#btnSelectNum', description='옵션 적용 버튼')
    BUY_BUTTON = Selector(value='#btnBuy', description='구매하기 버튼')
    BUY_CONFIRM_BUTTON = Selector(value='#popupLayerConfirm input[value="확인"]',
                                  description='구매 확정 버튼')
    TOTAL_PRICE = Selector(value='#payAmt', description='결제 금액')
    FAILURE = Selector(value='#popupLayerAlert', description='경고 팝업')


class MyBuyPageElements:
    HISTORY_TABLE = Selector(value='.tbl_data', description='당첨 결과 테이블')
    FAILURE = Selector(value='.nodata', description='결과 없음 메세지')


class TableElement:

    def __init__(self, driver: WebDriver) -> None:
        table = driver.find_element(By.CSS_SELECTOR, 'table')
        self.headers = table.find_elements(By.CSS_SELECTOR, 'thead th')
        self.rows = table.find_elements(By.CSS_SELECTOR, 'tbody tr')

    def headers_to_texts(self) -> List[str]:
        return [th.text for th in self.headers]

    def rows_to_texts(self) -> List[List[str]]:
        return [[td.text for td in row.find_elements(By.CSS_SELECTOR, 'td')]
                for row in self.rows]


def zip_table(header: List[str], rows: List[List[str]]):
    return [dict(zip_longest(header, cells, fillvalue='')) for cells in rows]
