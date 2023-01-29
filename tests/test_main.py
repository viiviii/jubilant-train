import pytest

from main import login, LottoError, buy


def test_login_success():
    # todo: 개인정보인데 어떻게 테스트 작성?
    pass


def test_login_failure_when_wrong_login_info():
    with pytest.raises(LottoError, match='[로그인 실패] *'):
        login('wrong125id2541', 'wrong@password')


def test_buy_failure_when_not_logged_in():
    with pytest.raises(LottoError, match='[로또 구매 실패] *'):
        buy()
