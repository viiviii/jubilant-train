import os
import uuid

import pytest

from lotto.secret import Secret
from sends.github.issue import Issue, create
from sends.github.main import Inputs
from tests.functional.sends.helper import close_issues_by_label, delete_label


@pytest.fixture(scope='session')
def issue():
    token = Secret(os.environ[Inputs.TOKEN])
    repository = os.environ[Inputs.REPOSITORY]
    label = f'testing:{uuid.uuid4()}'

    yield Issue(token=token, repository=repository,
                title='이슈 생성 테스트', content='이슈 생성 본문', label=label)

    close_issues_by_label(token, repository, label)
    delete_label(token, repository, label)


def test_create(issue):
    response = create(issue)

    assert response['number']
    assert response['state'] == 'open'
    assert response['title'] == issue.title
    assert response['body'] == issue.content
    assert len(response['labels']) == 1
    assert response['labels'][0]['name'] == issue.label
