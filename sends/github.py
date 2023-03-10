from typing import Optional, List

import requests

from lotto.secret import Secret
from sends.send import Send, SendResult, SendError


class Github:

    def __init__(self, token: str, repository: str) -> None:
        """
        Parameters:
            token (str): A token to authenticate on your repository.
            repository (str): The owner and repository name.

        Example:
            token: ghq_nZn7aQ...
            repository: octocat/Hello-World
        """
        self._token = Secret(token)
        self._repository = repository

    @property
    def token(self):
        return self._token.value

    @property
    def repository(self):
        return self._repository

    def __str__(self) -> str:
        return f'token={self._token}, repository={self.repository}'

    def __repr__(self) -> str:
        return f'Github({self})'


class Issue(Send):

    def __init__(self, github: Github, labels: Optional[List[str]] = None) -> None:
        self._github = github
        self._labels = labels or []

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
            f'https://api.github.com/repos/{self._github.repository}/issues',
            headers={
                'Accept': 'application/vnd.github+json',
                'Authorization': f'Bearer {self._github.token}',
                'X-GitHub-Api-Version': '2022-11-28',
            },
            json={
                'title': title,
                'body': content,
                'labels': self._labels
            },
        )
