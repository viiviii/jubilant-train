import pytest
from _pytest.config.argparsing import Parser

from lotto import account as lotto_account
from lotto.account import Account, fetch_account


@pytest.fixture(scope='session')
def account() -> Account:
    return fetch_account()


def pytest_addoption(parser):
    _add_id_option_for_passing_argument_to_pytest(parser)


def _add_id_option_for_passing_argument_to_pytest(parser: Parser):
    parser.addoption(lotto_account.ID_ARGUMENT_NAME,
                     **lotto_account.ID_ARGUMENT_OPTIONS)
