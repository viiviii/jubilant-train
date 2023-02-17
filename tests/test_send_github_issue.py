import pytest

from lotto.secret import Secret
from sends.send import SendError
from sends.send_github_issue import SendGithubIssue

_title = '🎊 로또6/45 1055회(23-02-18)'
_content = (
    '💰 총 당첨금: 1,234,567원\n'
    '✅ 총 구입매수: 5장\n'
    '📅 조회기간: 23-02-12 ~ 23-02-18')


class TestSendGithubIssue:

    def test_success_with_mock(self, requests_mock):
        requests_mock.post(
            'https://api.github.com/repos/octocat/Hello-World/issues',
            json={'title': _title, 'body': _content, }
        )

        send = SendGithubIssue(token=Secret('mock'), repository='octocat/Hello-World')
        actual = send(title=_title, content=_content)

        assert actual.title == _title
        assert actual.content == _content

    def test_failure(self):
        send = SendGithubIssue(token=Secret('invalid'), repository='octocat/Hello-World')

        with pytest.raises(SendError, match='이슈 생성 실패'):
            send(title=_title, content=_content)
