from lotto.lotto import *
from main import login


def test_go_login():
    go_login()
    assert '동행복권' in title()
    assert '로그인' in title()


def test_login_input_boxs():
    go_login()
    boxs = login_input_boxs()
    assert len(boxs) == 2
    assert boxs[0].accessible_name == '아이디'
    assert boxs[1].accessible_name == '비밀번호'


def test_login_button():
    go_login()
    button = login_button()
    assert button
    assert button.accessible_name == '로그인'


def test_amount_select():
    login('my_id', 'my_password')  # todo
    go_lotto()

    select = amount_select()

    assert select
    assert len(select.options) == 5


def test_auto_checkbox():
    login('my_id', 'my_password')  # todo
    go_lotto()

    checkbox = auto_checkbox()
    assert checkbox
    assert not checkbox.is_selected()


def test_apply_button():
    login('my_id', 'my_password')  # todo
    go_lotto()

    assert apply_button()


def test_buy_button():
    login('my_id', 'my_password')  # todo
    go_lotto()

    assert buy_button()


# todo
def test_confirm_button():
    login('my_id', 'my_password')  # todo
    go_lotto()
    auto_checkbox().click()
    apply_button().click()
    buy_button().click()

    confirm = confirm_button()

    assert confirm
    assert confirm.is_displayed()


def test_total_price():
    login('my_id', 'my_password')  # todo
    go_lotto()

    assert total_price() == 0
