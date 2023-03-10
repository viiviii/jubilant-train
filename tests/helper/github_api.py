import requests


def _headers(token):
    return {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2022-11-28',
    }


def issues_by_labels(github, labels):
    response = requests.get(
        f'https://api.github.com/repos/{github.repository}/issues',
        headers=_headers(github.token),
        params={
            'state': 'open',
            'labels': labels,
        },
    )

    assert response.ok, f'이슈 조회 실패=[{response.reason}] {response.text}'

    return response.json()


def close_issue(github, number):
    response = requests.patch(
        f'https://api.github.com/repos/{github.repository}/issues/{number}',
        headers=_headers(github.token),
        json={
            'state': 'closed',
            'state_reason': 'completed',
        }
    )

    assert response.ok, f'이슈 종료 실패=[{response.reason}] {response.text}'


def create_label(github, name, description):
    response = requests.post(
        f'https://api.github.com/repos/{github.repository}/labels',
        headers=_headers(github.token),
        json={
            'name': name,
            'description': description,
            'color': 'ffffff',
        }
    )

    assert response.ok, f'라벨 생성 실패=[{response.reason}] {response.text}'


def delete_label(github, name):
    response = requests.delete(
        f'https://api.github.com/repos/{github.repository}/labels/{name}',
        headers=_headers(github.token),
    )

    assert response.ok, f'라벨 삭제 실패=[{response.reason}] {response.text}'
