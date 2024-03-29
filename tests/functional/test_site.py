from datetime import date

import pytest

from lotto.lotto import *
from lotto.secret import Secret
from lotto.site.site import Site


@pytest.fixture(scope='class')
def lotto(driver) -> Lotto:
    return Site(driver)


# noinspection NonAsciiCharacters
class TestSuccess:

    def test_login(self, lotto, account):
        lotto.login(account)

    @pytest.mark.buy_required
    def test_buy(self, lotto):
        구입_매수 = 1
        로또_가격 = 1_000

        결제_금액 = lotto.buy(amount=구입_매수)

        assert 결제_금액 == 구입_매수 * 로또_가격

    @pytest.mark.buy_required
    def test_result(self, lotto):
        조회_기간은_오늘 = DateRange(date.today(), date.today())

        구매_결과 = lotto.result(dates=조회_기간은_오늘)

        assert 구매_결과


class TestFailure:

    def test_result_failure_when_not_logged_in(self, lotto):
        with pytest.raises(LottoError, match='당첨 조회 실패'):
            lotto.result(dates=DateRange(date.today(), date.today()))

    def test_buy_failure_when_not_logged_in(self, lotto):
        with pytest.raises(LottoError, match='로또 구매 실패'):
            lotto.buy(amount=1)

    def test_login_failure_when_invalid_account(self, lotto):
        with pytest.raises(LottoError, match='로그인 실패'):
            lotto.login(Account('잘못된_아이디', Secret('잘못된_비밀번호')))
