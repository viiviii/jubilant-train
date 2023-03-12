import requests

from lotto.secret import Secret


def delete_label(token: Secret, repository: str, name: str):
    response = requests.delete(
        f'https://api.github.com/repos/{repository}/labels/{name}',
        headers=_headers(token),
    )

    assert response.ok, f'라벨 삭제 실패=[{response.reason}] {response.text}'


def close_issues_by_label(token: Secret, repository: str, label: str):
    issues = _issues_by_label(token, repository, label)
    for issue in issues:
        _close_issue(token, repository, issue['number'])


def _issues_by_label(token: Secret, repository: str, label: str):
    response = requests.get(
        f'https://api.github.com/repos/{repository}/issues',
        headers=_headers(token),
        params={
            'state': 'open',
            'labels': [label],
        },
    )

    assert response.ok, f'이슈 조회 실패=[{response.reason}] {response.text}'

    return response.json()


def _close_issue(token: Secret, repository: str, number: int):
    response = requests.patch(
        f'https://api.github.com/repos/{repository}/issues/{number}',
        headers=_headers(token),
        json={
            'state': 'closed',
            'state_reason': 'completed',
        }
    )

    assert response.ok, f'이슈 종료 실패=[{response.reason}] {response.text}'


def _headers(token: Secret):
    return {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token.value}',
        'X-GitHub-Api-Version': '2022-11-28',
    }
