from datetime import date

import pytest

from lotto.lotto_site import LottoSite
from lotto.lotto_site_page import LoginPage, title, LottoPage, MyBuyPage


@pytest.fixture(scope='class')
def login(account) -> None:
    LottoSite().login(account)


class TestLoginPage:

    @pytest.fixture(scope='class')
    def page(self):
        return LoginPage()

    @pytest.fixture(scope='class', autouse=True)
    def setup(self, page):
        page.go_login()

    def test_page_title(self):
        page_title = title()
        assert '동행복권' in page_title
        assert '로그인' in page_title

    def test_login_input_boxs(self, page):
        boxs = page.login_input_boxs()
        assert len(boxs) == 2
        assert boxs[0].accessible_name == '아이디'
        assert boxs[1].accessible_name == '비밀번호'

    def test_login_button(self, page):
        button = page.login_button()
        assert button
        assert button.accessible_name == '로그인'


class TestLottoPage:

    @pytest.fixture(scope='class')
    def page(self):
        return LottoPage()

    @pytest.fixture(scope='class', autouse=True)
    def setup(self, page, login):
        page.go_lotto()

    def test_auto_checkbox(self, page):
        assert page.auto_checkbox()

    def test_amount_select(self, page):
        select = page.amount_select()
        assert select
        assert len(select.options) == 5

    def test_apply_button(self, page):
        assert page.apply_button()

    def test_buy_button(self, page):
        assert page.buy_button()

    def test_confirm_button(self, page):
        assert page.confirm_button()


class TestMyBuyPage:
    searching_date_range = date(2023, 1, 1), date(2023, 1, 1)

    @pytest.fixture(scope='class')
    def page(self):
        return MyBuyPage()

    # todo: 로그인 안했을 때 실패 테스트 어디서 할까 -> 현재 중복되어 있음
    def test_failure_message(self, page):
        page.go_my_buy(*self.searching_date_range)

        assert '로그인 후 이용' in page.no_data_message()

    def test_buy_results(self, page, login):
        page.go_my_buy(*self.searching_date_range)

        results = page.buy_results()

        assert results
        assert '복권명' in results[0]
        assert '당첨금' in results[0]
        assert '당첨결과' in results[0]
        assert '구입매수' in results[0]

    def test_total_buy_result_when_not_buy(self, page):
        buys = [{'구입일자': '조회 결과가 없습니다.', '복권명': '', '회차': '', '선택번호/복권번호': '',
                 '구입매수': '', '당첨결과': '', '당첨금': '', '추첨일': ''}]

        assert page.total_buy_result(buys) == {
            '총 당첨금': 0,
            '총 구입매수': 0,
            '미추첨': 0,
        }

    def test_total_buy_result_when_buy(self, page):
        buys = [
            {'구입일자': '2023-02-07', '복권명': '로또6/45', '회차': '1054', '선택번호/복권번호': '51738 11491 27411 72232 76893 71219',
             '구입매수': '5', '당첨결과': '미추첨', '당첨금': '-', '추첨일': '2023-02-11'},
            {'구입일자': '2023-02-06', '복권명': '로또6/45', '회차': '1054', '선택번호/복권번호': '51711 11490 27422 87222 61893 52349',
             '구입매수': '2', '당첨결과': '미추첨', '당첨금': '-', '추첨일': '2023-02-11'},
            {'구입일자': '2023-02-04', '복권명': '로또6/45', '회차': '1053', '선택번호/복권번호': '50012 91499 11223 13078 41298 32090',
             '구입매수': '1', '당첨결과': '당첨', '당첨금': '50,000원', '추첨일': '2023-02-04'},
            {'구입일자': '2023-02-04', '복권명': '로또6/45', '회차': '1053', '선택번호/복권번호': '59912 84214 07899 86707 14326 52110',
             '구입매수': '2', '당첨결과': '낙첨', '당첨금': '-', '추첨일': '2023-02-04'},
            {'구입일자': '2023-02-04', '복권명': '로또6/45', '회차': '1053', '선택번호/복권번호': '61234 23524 25931 66317 64326 62190',
             '구입매수': '5', '당첨결과': '당첨', '당첨금': '5,000원', '추첨일': '2023-02-04'},
            {'구입일자': '2023-01-01', '복권명': '연금복권720', '회차': '90', '선택번호/복권번호': '5조000011',
             '구입매수': '2', '당첨결과': '낙첨', '당첨금': '-', '추첨일': '2022-08-25'},
        ]

        assert page.total_buy_result(buys) == {
            '총 당첨금': 55000,
            '총 구입매수': 17,
            '미추첨': 7,
        }

    def test_extract_amount(self, page):
        assert page.extract_amount('-') == 0
        assert page.extract_amount('') == 0
        assert page.extract_amount('0원') == 0
        assert page.extract_amount('5,000원') == 5000
        assert page.extract_amount('1,234,567원') == 1234567