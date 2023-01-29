import pytest

from main import login, LoginError


def test_sign_in_success():
    # todo: 개인정보인데 어떻게 테스트 작성?
    pass


def test_sign_in_failure():
    with pytest.raises(LoginError, match='[로그인 실패] *'):
        login('wrong125id2541', 'wrong@password')
