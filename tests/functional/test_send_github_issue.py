import pytest

import sends.github
from sends.github import Github
from sends.send import SendError, Send
from tests.functional.conftest import close_issues_by_labels


@pytest.fixture
def send(github, labels) -> Send:
    yield sends.github.Issue(github=github, labels=labels)
    close_issues_by_labels(github=github, labels=labels)


# noinspection NonAsciiCharacters
def test_success(send):
    결과 = send(title='이슈 생성 성공 테스트', content='이슈 본문')

    assert 결과.title == '이슈 생성 성공 테스트'
    assert 결과.content == '이슈 본문'


# noinspection NonAsciiCharacters
def test_failure(github):
    유효하지_않은_토큰 = 'invalid-token'

    send = sends.github.Issue(Github(token=유효하지_않은_토큰, repository=github.repository))

    with pytest.raises(SendError, match='이슈 생성 실패'):
        send(title='제목', content='내용')
