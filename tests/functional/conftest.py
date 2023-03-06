from datetime import date, datetime

import pytest
import requests
from _pytest.config.argparsing import Parser
from selenium import webdriver

from lotto.account import Account, fetch_account, ID_ARGUMENT_OPTIONS, ID_ARGUMENT_NAME
from lotto.secret import Secret


@pytest.fixture(scope='class')
def driver():
    _driver = webdriver.Chrome()
    yield _driver
    _driver.quit()


@pytest.fixture(scope='session')
def account() -> Account:
    return fetch_account()


def pytest_addoption(parser):
    _add_id_option_for_passing_argument_to_pytest(parser)


def _add_id_option_for_passing_argument_to_pytest(parser: Parser):
    parser.addoption(ID_ARGUMENT_NAME, **ID_ARGUMENT_OPTIONS)


@pytest.fixture(scope='session')
def token():
    # todo: env에서 가져오기
    return Secret('token')


@pytest.fixture(scope='session')
def repository():
    # todo: env에서 가져오기
    return 'viiviii/something'


@pytest.fixture(scope='session')
def labels():
    return ['for-testing']


def close_testing_issues(token, repository, labels, since):
    issues = issues_created_by_tests(token=token, repository=repository, labels=labels, since=since)

    for issue in issues:
        close_issue(token=token, repository=repository, number=issue['number'])


def issues_created_by_tests(token, repository, labels, since: datetime = date.today()):
    response = requests.get(
        f'https://api.github.com/repos/{repository}/issues',
        headers={
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {token.value}',
            'X-GitHub-Api-Version': '2022-11-28',
        },
        params={
            'state': 'open',
            'creator': repository.split('/')[0],
            'labels': labels,
            'since': since.isoformat()
        },
    )

    assert response.ok, f'이슈 조회 실패=[{response.reason}] {response.text}'

    return response.json()


def close_issue(token, repository, number):
    response = requests.patch(
        f'https://api.github.com/repos/{repository}/issues/{number}',
        headers={
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {token.value}',
            'X-GitHub-Api-Version': '2022-11-28',
        },
        json={
            'state': 'closed',
            'state_reason': 'completed',
        }
    )

    assert response.ok, f'이슈 종료 실패=[{response.reason}] {response.text}'
