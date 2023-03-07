import uuid

import pytest

import lotto.account
import sends.auth
from lotto.site import drivers
from tests.helper import github_api as api


@pytest.fixture(scope='session')
def account() -> lotto.account.Account:
    return lotto.account.from_env()


@pytest.fixture(scope='session')
def auth() -> sends.auth.Auth:
    return sends.auth.from_env()


@pytest.fixture(scope='session')
def labels():
    return ['for-testing']


@pytest.fixture(scope='class')
def driver():
    _driver = drivers.headless_chrome()
    yield _driver
    _driver.quit()


@pytest.fixture
def labels(auth):
    name = f'testing:{uuid.uuid4()}'
    api.create_label(auth=auth, name=name, description='Unique labels for testing')
    yield [name]
    api.delete_label(auth=auth, name=name)


def close_issues_by_labels(auth, labels):
    issues = api.issues_by_labels(auth=auth, labels=labels)

    for issue in issues:
        api.close_issue(auth=auth, number=issue['number'])
