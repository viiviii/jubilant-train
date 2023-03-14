import os

import pytest
import requests

from lotto.secret import Secret
from sends.github.issue import Issue, create
from sends.github.main import Inputs


@pytest.fixture(scope='class')
def issue(label):
    return Issue(
        token=Secret(os.environ[Inputs.TOKEN]),
        repository=os.environ[Inputs.REPOSITORY],
        title='이슈 생성 테스트 제목', content='이슈 생성 테스트 본문', label=label)


@pytest.fixture(scope='class')
def created_issue(issue):
    response = create(issue)
    yield response
    _close_issue(issue.token, issue.repository, response['number'])


class TestWithLabel:

    @pytest.fixture(scope='class')
    def label(self):
        return 'for-testing'

    def test_success(self, issue, created_issue):
        assert_opened(created_issue)
        assert_equals(created_issue, issue)


class TestWithoutLabel:

    @pytest.fixture(scope='class')
    def label(self):
        return None

    def test_success(self, issue, created_issue):
        assert_opened(created_issue)
        assert_equals(created_issue, issue)


def assert_opened(response):
    assert response['number']
    assert response['state'] == 'open'


def assert_equals(response, issue):
    assert response['title'] == issue.title
    assert response['body'] == issue.content

    labels = [label['name'] for label in response['labels']]
    assert labels == ([issue.label] if issue.label else [])


def _close_issue(token: Secret, repository: str, number: str):
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
