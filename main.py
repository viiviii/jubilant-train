from lotto.lotto import go_login, login_input_boxs, login_button, alert


class LoginError(Exception):
    def __init__(self, reason: str):
        super().__init__(f'[로그인 실패] {reason}')


# todo: 클라이언트에서 send_keys 사용성
# todo: 로그인 성공/실패 기준 어떤걸로?
def login(_id: str, password: str) -> None:
    go_login()
    _id_box, password_box = login_input_boxs()

    _id_box.send_keys(_id)
    password_box.send_keys(password)

    login_button().click()

    login_failure_alert = alert()
    if login_failure_alert:
        raise LoginError(reason=login_failure_alert.text)


if __name__ == '__main__':
    # todo: 개인정보인데 어떻게 관리?
    _id = 'my_id'
    _password = 'my_password'

    # 시작
    login(_id, _password)
