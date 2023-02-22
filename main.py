from lotto.account import Account, fetch_account
from lotto.lotto import *


class LottoError(Exception):
    def __init__(self, reason: str, detail: str):
        super().__init__(f'[{reason}] {detail}')


# todo: 클라이언트에서 send_keys 사용성
# todo: 로그인 성공/실패 기준 어떤걸로?
def login(account: Account) -> None:
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


def buy(amount: int) -> None:
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


def check_lottery_result(start_date: date, end_date: date) -> dict[str, int]:
    go_my_buy(start_date=start_date, end_date=end_date)

    # todo
    failure_message = no_data_message()
    if failure_message:
        raise LottoError(reason='당첨 조회 실패', detail=failure_message)

    return {'시작일': start_date, '종료일': end_date} | total_buy_result(buy_results())


if __name__ == '__main__':
    login(fetch_account())
    # buy(amount=1)
