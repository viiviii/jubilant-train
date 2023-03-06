from datetime import date, datetime

import pytest
import requests
from _pytest.config.argparsing import Parser
from selenium import webdriver

import lotto.account
import sends.auth
from lotto.account import ID_ARGUMENT_OPTIONS, ID_ARGUMENT_NAME


@pytest.fixture(scope='class')
def driver():
    _driver = webdriver.Chrome()
    yield _driver
    _driver.quit()


@pytest.fixture(scope='session')
def account() -> lotto.account.Account:
    return lotto.account.from_env()


@pytest.fixture(scope='session')
def auth() -> sends.auth.Auth:
    return sends.auth.from_env()


def pytest_addoption(parser):
    _add_id_option_for_passing_argument_to_pytest(parser)


def _add_id_option_for_passing_argument_to_pytest(parser: Parser):
    parser.addoption(ID_ARGUMENT_NAME, **ID_ARGUMENT_OPTIONS)


@pytest.fixture(scope='session')
def labels():
    return ['for-testing']


def close_testing_issues(auth, labels, since):
    issues = issues_created_by_tests(auth=auth, labels=labels, since=since)

    for issue in issues:
        close_issue(auth=auth, number=issue['number'])


def issues_created_by_tests(auth, labels, since: datetime = date.today()):
    response = requests.get(
        f'https://api.github.com/repos/{auth.repository}/issues',
        headers={
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {auth.token}',
            'X-GitHub-Api-Version': '2022-11-28',
        },
        params={
            'state': 'open',
            'creator': auth.owner,
            'labels': labels,
            'since': since.isoformat()
        },
    )

    assert response.ok, f'이슈 조회 실패=[{response.reason}] {response.text}'

    return response.json()


def close_issue(auth, number):
    response = requests.patch(
        f'https://api.github.com/repos/{auth.repository}/issues/{number}',
        headers={
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {auth.token}',
            'X-GitHub-Api-Version': '2022-11-28',
        },
        json={
            'state': 'closed',
            'state_reason': 'completed',
        }
    )

    assert response.ok, f'이슈 종료 실패=[{response.reason}] {response.text}'
