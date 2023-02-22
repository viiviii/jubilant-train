import pytest
from _pytest.config.argparsing import Parser

from lotto.account import Account, fetch_account, ID_ARGUMENT_OPTIONS, ID_ARGUMENT_NAME


@pytest.fixture(scope='session')
def account() -> Account:
    return fetch_account()


def pytest_addoption(parser):
    _add_id_option_for_passing_argument_to_pytest(parser)


def _add_id_option_for_passing_argument_to_pytest(parser: Parser):
    parser.addoption(ID_ARGUMENT_NAME, **ID_ARGUMENT_OPTIONS)
