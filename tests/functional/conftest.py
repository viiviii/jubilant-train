import uuid

import pytest
from dotenv import load_dotenv

import env
import lotto.account
import sends.github
from lotto.site import drivers
from tests.helper import github_api as api

load_dotenv()


@pytest.fixture(scope='session')
def account() -> lotto.account.Account:
    return env.ACCOUNT


@pytest.fixture(scope='session')
def github() -> sends.github.Github:
    return env.GITHUB


@pytest.fixture(scope='session')
def labels():
    return ['for-testing']


@pytest.fixture(scope='class')
def driver():
    _driver = drivers.headless_chrome()
    yield _driver
    _driver.quit()


@pytest.fixture
def labels(github):
    label_name = f'testing:{uuid.uuid4()}'
    api.create_label(github=github, name=label_name,
                     description='Unique labels for testing')
    yield [label_name]
    api.delete_label(github=github, name=label_name)


def close_issues_by_labels(github, labels):
    issues = api.issues_by_labels(github=github, labels=labels)
    for issue in issues:
        api.close_issue(github=github, number=issue['number'])
