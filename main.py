from lotto.lotto import go_login, login_input_boxs, login_button, alert, go_lotto, layer_popup, amount_select, \
    auto_checkbox, apply_button


class LottoError(Exception):
    def __init__(self, reason: str, detail: str):
        super().__init__(f'[{reason}] {detail}')


# todo: 클라이언트에서 send_keys 사용성
# todo: 로그인 성공/실패 기준 어떤걸로?
def login(_id: str, password: str) -> None:
    go_login()
    _id_box, password_box = login_input_boxs()

    _id_box.send_keys(_id)
    password_box.send_keys(password)

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


if __name__ == '__main__':
    # todo: 개인정보인데 어떻게 관리?
    _id = 'my_id'
    _password = 'my_password'

    # 시작
    login(_id, _password)
    buy(amount=5)
