from datetime import date
from typing import Any

from lotto.lotto import Account
from lotto.lotto import Lotto, LottoError
from lotto.lotto_site_page import LoginPage, alert, LottoPage, MyBuyPage


class LottoSite(Lotto):

    def login(self, account: Account) -> None:
        page = LoginPage()
        page.go_login()

        _id_box, password_box = page.login_input_boxs()
        _id_box.send_keys(account.id)
        password_box.send_keys(account.password)

        page.login_button().click()

        # todo
        failure_alert = alert()
        if failure_alert:
            raise LottoError(reason='로그인 실패', detail=failure_alert.text)

    def buy(self, amount: int) -> int:
        page = LottoPage()
        page.go_lotto()

        # todo
        failure_popup = page.layer_popup()
        if failure_popup.is_displayed():
            raise LottoError(reason='로또 구매 실패', detail=failure_popup.text)

        page.amount_select().select_by_value(str(amount))
        page.auto_checkbox().click()

        page.apply_button().click()

        page.buy_button().click()
        page.confirm_button().click()

        # todo
        failure_popup = page.layer_popup()
        if failure_popup.is_displayed():
            raise LottoError(reason='로또 구매 실패', detail=failure_popup.text)

        return page.total_price()

    def result(self, start: date, end: date) -> dict[str, Any]:
        page = MyBuyPage()
        page.go_my_buy(start_date=start, end_date=end)

        # todo
        failure_message = page.no_data_message()
        if failure_message:
            raise LottoError(reason='당첨 조회 실패', detail=failure_message)

        return {'조회 시작일': start, '조회 종료일': end} | page.total_buy_result(page.buy_results())
