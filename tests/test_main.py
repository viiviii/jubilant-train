from datetime import datetime

import pytest

from main import *


class TestSuccess:

    def test_login(self, account):
        login(account)  # todo
        # todo: 로그인 유무 어떻게 체크?

    # todo: 테스트 돌릴 때마다 진짜 살거니?
    # todo: 진짜 살거면 설정 추가하거나 buy, select로 기능 나누기
    def test_buy(self):
        buy(amount=5)
        assert total_price() == 5 * 1000

    def test_check_lottery_result(self):
        today = datetime.today()
        result = check_lottery_result(start_date=today, end_date=today)
        assert result['시작일'] == today
        assert result['종료일'] == today
        assert result['총 당첨금'] >= 0
        assert result['총 구입매수'] >= 0
        assert result['미추첨'] >= 0


# todo: 아 여긴 진짜 격리해야겠다
class TestFailure:

    def test_login_failure_when_invalid_account(self):
        with pytest.raises(LottoError, match='[로그인 실패] *'):
            invalid_account = Account('invalid125id', 'invalid@password')
            login(invalid_account)

    def test_buy_failure_when_not_logged_in(self):
        with pytest.raises(LottoError, match='[로또 구매 실패] *'):
            buy(amount=1)


# todo: 테스트 위치 어디에...?
def test_to_message():
    actual = to_message(result={
        '총 당첨금': 1234567,
        '총 구입매수': 11, '미추첨': 0,
        '시작일': date(2020, 1, 1), '종료일': date(2021, 11, 28)})

    assert actual == (
        '💰 총 당첨금: 1,234,567원\n'
        '✅ 총 구입매수: 11장 (미추첨 0장)\n'
        '📅 조회기간: 20-01-01 ~ 21-11-28')


def test_last_sunday():
    sunday = date(2023, 1, 1)
    monday = date(2023, 1, 2)

    assert last_sunday(today=monday) == sunday
    assert last_sunday(today=sunday) == sunday
