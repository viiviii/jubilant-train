import requests


def _headers(auth):
    return {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {auth.token}',
        'X-GitHub-Api-Version': '2022-11-28',
    }


def issues_by_labels(auth, labels):
    response = requests.get(
        f'https://api.github.com/repos/{auth.repository}/issues',
        headers=_headers(auth),
        params={
            'state': 'open',
            'labels': labels,
        },
    )

    assert response.ok, f'이슈 조회 실패=[{response.reason}] {response.text}'

    return response.json()


def close_issue(auth, number):
    response = requests.patch(
        f'https://api.github.com/repos/{auth.repository}/issues/{number}',
        headers=_headers(auth),
        json={
            'state': 'closed',
            'state_reason': 'completed',
        }
    )

    assert response.ok, f'이슈 종료 실패=[{response.reason}] {response.text}'


def create_label(auth, name, description):
    response = requests.post(
        f'https://api.github.com/repos/{auth.repository}/labels',
        headers=_headers(auth),
        json={
            'name': name,
            'description': description,
            'color': 'ffffff',
        }
    )

    assert response.ok, f'라벨 생성 실패=[{response.reason}] {response.text}'


def delete_label(auth, name):
    response = requests.delete(
        f'https://api.github.com/repos/{auth.repository}/labels/{name}',
        headers=_headers(auth),
    )

    assert response.ok, f'라벨 삭제 실패=[{response.reason}] {response.text}'
