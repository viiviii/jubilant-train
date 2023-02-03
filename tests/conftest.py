from typing import Optional

import pytest
from _pytest.config.argparsing import Parser

from lotto import account as lotto_account


@pytest.fixture(scope='module')
def account() -> tuple[str, Optional[str]]:
    return lotto_account.account()


def pytest_addoption(parser):
    _add_id_option_for_passing_argument_to_pytest(parser)


def _add_id_option_for_passing_argument_to_pytest(parser: Parser):
    parser.addoption(lotto_account.ID_ARGUMENT_NAME,
                     **lotto_account.ID_ARGUMENT_OPTIONS)
