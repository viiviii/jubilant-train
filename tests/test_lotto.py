from lotto.lotto import *


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
