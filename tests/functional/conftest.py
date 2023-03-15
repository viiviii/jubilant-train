import pytest
from dotenv import load_dotenv

import env
import lotto.account
from lotto.site import drivers

load_dotenv()


@pytest.fixture(scope='session')
def account() -> lotto.account.Account:
    return env.to_account()


@pytest.fixture(scope='class')
def driver():
    _driver = drivers.headless_chrome()
    yield _driver
    _driver.quit()
