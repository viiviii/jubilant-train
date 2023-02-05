import pytest

from lotto.lotto import *
from main import login


class TestLoginPage:

    @pytest.fixture(scope='class', autouse=True)
    def setup(self):
        go_login()

    def test_title(self):
        page_title = title()
        assert '동행복권' in page_title
        assert '로그인' in page_title

    def test_login_input_boxs(self):
        boxs = login_input_boxs()
        assert len(boxs) == 2
        assert boxs[0].accessible_name == '아이디'
        assert boxs[1].accessible_name == '비밀번호'

    def test_login_button(self):
        button = login_button()
        assert button
        assert button.accessible_name == '로그인'


class TestLottoPage:

    @pytest.fixture(scope='class', autouse=True)
    def setup(self, account):
        go_login()
        login(account)
        go_lotto()

    def test_auto_checkbox(self):
        assert auto_checkbox()

    def test_amount_select(self):
        select = amount_select()
        assert select
        assert len(select.options) == 5

    def test_apply_button(self):
        assert apply_button()

    def test_buy_button(self):
        assert buy_button()

    def test_confirm_button(self):
        assert confirm_button()
