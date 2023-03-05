from datetime import datetime, timezone

import pytest

from lotto.secret import Secret
from sends.send import SendError, Send
from sends.send_github_issue import SendGithubIssue
from tests.functional.conftest import close_testing_issues


@pytest.fixture
def send(token, repository, labels) -> Send:
    _start = datetime.now(timezone.utc)
    yield SendGithubIssue(token=token, repository=repository, labels=labels)
    close_testing_issues(since=_start, token=token, repository=repository, labels=labels)


# noinspection NonAsciiCharacters
def test_success(send):
    결과 = send(title='이슈 생성 성공 테스트', content='이슈 본문')

    assert 결과.title == '이슈 생성 성공 테스트'
    assert 결과.content == '이슈 본문'


# noinspection NonAsciiCharacters
def test_failure():
    유효하지_않은_토큰 = Secret('invalid-token')
    권한이_없는_리포 = 'octocat/Hello-World'

    send = SendGithubIssue(token=유효하지_않은_토큰, repository=권한이_없는_리포)

    with pytest.raises(SendError, match='이슈 생성 실패'):
        send(title='제목', content='내용')
