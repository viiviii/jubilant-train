from lotto.lotto import *


def test_go_login():
    go_login()
    assert '동행복권' in title()
    assert '로그인' in title()
