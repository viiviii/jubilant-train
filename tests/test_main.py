import pytest

from lotto.account import Account
from lotto.lotto import go_lotto, total_price
from main import login, buy, LottoError


class TestSuccess:

    def test_login(self, account):
        login(account)  # todo
        # todo: 로그인 유무 어떻게 체크?

    # todo: 테스트 돌릴 때마다 진짜 살거니?
    # todo: 진짜 살거면 설정 추가하거나 buy, select로 기능 나누기
    def test_buy(self):
        go_lotto()
        buy(amount=5)
        assert total_price() == 5 * 1000


# todo: 아 여긴 진짜 격리해야겠다
class TestFailure:
    
    def test_login_failure_when_invalid_account(self):
        with pytest.raises(LottoError, match='[로그인 실패] *'):
            invalid_account = Account('invalid125id', 'invalid@password')
            login(invalid_account)

    def test_buy_failure_when_not_logged_in(self):
        with pytest.raises(LottoError, match='[로또 구매 실패] *'):
            buy(amount=1)
