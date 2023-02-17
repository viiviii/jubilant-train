import requests

from lotto.secret import Secret
from sends.send import Send, SendResult, SendError


class SendGithubIssue(Send):

    def __init__(self, token: Secret, repository: str) -> None:
        self.token = token
        self.repository = repository

    def __call__(self, title: str, content: str) -> SendResult:
        response = self._create_issue(title, content)
        json = response.json()

        if not response.ok:
            raise SendError(reason='이슈 생성 실패', detail=json['message'])

        return SendResult(title=json['title'], content=json['body'])

    def _create_issue(self, title: str, content: str) -> requests.Response:
        """
        https://docs.github.com/ko/rest/issues/issues?apiVersion=2022-11-28#create-an-issue
        """
        return requests.post(
            f'https://api.github.com/repos/{self.repository}/issues',
            headers={
                'Accept': 'application/vnd.github+json',
                'Authorization': f'Bearer {self.token.value}',
                'X-GitHub-Api-Version': '2022-11-28',
            },
            json={
                'title': title,
                'body': content,
            },
        )
