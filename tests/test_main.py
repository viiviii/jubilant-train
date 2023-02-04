import pytest

from lotto.account import Account
from lotto.lotto import go_lotto, total_price
from main import login, LottoError, buy


def test_login_success():
    # todo: 개인정보인데 어떻게 테스트 작성?
    pass


# todo: 테스트 lotto로 이동하거나 제거
def test_buy(account):
    login(account)  # todo
    go_lotto()
    buy(amount=5)
    assert total_price() == 5 * 1000


def test_login_failure_when_invalid_account():
    with pytest.raises(LottoError, match='[로그인 실패] *'):
        invalid_account = Account('invalid125id2541', 'invalid@password')
        login(invalid_account)


def test_buy_failure_when_not_logged_in():
    with pytest.raises(LottoError, match='[로또 구매 실패] *'):
        buy(amount=1)
