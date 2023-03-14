from dataclasses import dataclass
from typing import Optional, Any

import requests

from lotto.secret import Secret


@dataclass(frozen=True)
class Issue:
    token: Secret
    repository: str
    title: str
    content: str
    label: Optional[str]


def create(issue: Issue) -> dict[str, Any]:
    """
    https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#create-an-issue
    """
    response = requests.post(
        f'https://api.github.com/repos/{issue.repository}/issues',
        headers={
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {issue.token.value}',
            'X-GitHub-Api-Version': '2022-11-28',
        },
        json={
            'title': issue.title,
            'body': issue.content,
            'labels': [issue.label] if issue.label else [],
        },
    )

    response.raise_for_status()

    return response.json()
