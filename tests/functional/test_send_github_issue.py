from datetime import datetime, timezone

import pytest

import sends.github
from sends.auth import Auth
from sends.send import SendError, Send
from tests.functional.conftest import close_testing_issues


@pytest.fixture
def send(auth, labels) -> Send:
    start = datetime.now(timezone.utc)
    yield sends.github.Issue(auth=auth, labels=labels)
    close_testing_issues(auth=auth, labels=labels, since=start)


# noinspection NonAsciiCharacters
def test_success(send):
    결과 = send(title='이슈 생성 성공 테스트', content='이슈 본문')

    assert 결과.title == '이슈 생성 성공 테스트'
    assert 결과.content == '이슈 본문'


# noinspection NonAsciiCharacters
def test_failure(auth):
    유효하지_않은_인증 = Auth(token='invalid-token', owner=auth.owner, repository=auth.repository)

    send = sends.github.Issue(auth=유효하지_않은_인증)

    with pytest.raises(SendError, match='이슈 생성 실패'):
        send(title='제목', content='내용')
