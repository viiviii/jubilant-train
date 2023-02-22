import pytest

from lotto.lotto import *
from lotto.lotto_site import LottoSite


@pytest.fixture(scope='class')
def lotto() -> Lotto:
    return LottoSite()


class TestSuccess:

    # todo: 로그인 유무 어떻게 체크?
    def test_login(self, lotto, account):
        lotto.login(account)

    # todo: 테스트 돌릴 때마다 진짜 살거니?
    def test_buy(self, lotto):
        assert lotto.buy(amount=5) == 5 * 1000

    # todo: no-data는 1) 로그인하지 않았을 때, 2)구매 이력이 없을 떄 두가지임
    def test_result(self, lotto):
        assert lotto.result(start=date.today(), end=date.today())


class TestFailure:

    def test_login_failure_when_invalid_account(self, lotto):
        with pytest.raises(LottoError, match='로그인 실패'):
            lotto.login(Account('invalid125id', 'invalid@password'))

    def test_buy_failure_when_not_logged_in(self, lotto):
        with pytest.raises(LottoError, match='로또 구매 실패'):
            lotto.buy(amount=1)

    def test_failure_lotto_result_when_not_logged_in(self, lotto):
        with pytest.raises(LottoError, match='당첨 조회 실패'):
            lotto.result(start=date.today(), end=date.today())
