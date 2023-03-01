import pytest
from selenium import webdriver

from lotto.lotto import *
from lotto.lotto_site import LottoSite


@pytest.fixture(scope='class')
def driver():
    _driver = webdriver.Chrome()
    yield _driver
    _driver.quit()


@pytest.fixture(scope='class')
def lotto(driver) -> Lotto:
    return LottoSite(driver)


# todo: 이거 진짜 돌릴거면 마커 달아놔라
# noinspection NonAsciiCharacters
class TestSuccess:

    @pytest.fixture(scope='class', autouse=True)
    def setup(self, lotto, account):
        lotto.login(account)

    def test_buy(self, lotto):
        구입_매수 = 1
        로또_가격 = 1_000

        결제_금액 = lotto.buy(amount=구입_매수)

        assert 결제_금액 == 구입_매수 * 로또_가격

    def test_result(self, lotto):
        오늘 = date.today()

        구매_결과 = lotto.result(start=오늘, end=오늘)

        assert 구매_결과


class TestFailure:

    def test_result_failure_when_not_logged_in(self, lotto):
        with pytest.raises(LottoError, match='당첨 조회 실패'):
            lotto.result(start=date.today(), end=date.today())

    def test_buy_failure_when_not_logged_in(self, lotto):
        with pytest.raises(LottoError, match='로또 구매 실패'):
            lotto.buy(amount=1)

    def test_login_failure_when_invalid_account(self, lotto):
        with pytest.raises(LottoError, match='로그인 실패'):
            lotto.login(Account('잘못된_아이디', '잘못된_비밀번호'))
