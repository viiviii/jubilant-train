from abc import ABCMeta, abstractmethod
from typing import Any

from lotto.account import Account
from lotto.lotto import *


class Lotto(metaclass=ABCMeta):

    @abstractmethod
    def login(self, account: Account) -> None:
        pass

    @abstractmethod
    def buy(self, amount: int) -> int:
        pass

    @abstractmethod
    def result(self, start: date, end: date) -> dict[str, Any]:
        pass


class LottoError(Exception):
    def __init__(self, reason: str, detail: str):
        super().__init__(f'[{reason}] {detail}')


class LottoWebsite(Lotto):

    def login(self, account: Account) -> None:
        assert account

        go_login()
        _id_box, password_box = login_input_boxs()

        _id_box.send_keys(account.id)
        password_box.send_keys(account.password)

        login_button().click()

        # todo
        failure_alert = alert()
        if failure_alert:
            raise LottoError(reason='로그인 실패', detail=failure_alert.text)

    def buy(self, amount: int) -> int:
        go_lotto()

        # todo
        failure_popup = layer_popup()
        if failure_popup.is_displayed():
            raise LottoError(reason='로또 구매 실패', detail=failure_popup.text)

        amount_select().select_by_value(str(amount))
        auto_checkbox().click()

        apply_button().click()

        buy_button().click()
        confirm_button().click()

        # todo
        failure_popup = layer_popup()
        if failure_popup.is_displayed():
            raise LottoError(reason='로또 구매 실패', detail=failure_popup.text)

        return total_price()

    def result(self, start: date, end: date) -> dict[str, Any]:
        go_my_buy(start_date=start, end_date=end)

        # todo
        failure_message = no_data_message()
        if failure_message:
            raise LottoError(reason='당첨 조회 실패', detail=failure_message)

        return {'조회 시작일': start, '조회 종료일': end} | total_buy_result(buy_results())
