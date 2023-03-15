from unittest import mock

import pytest

from lotto.secret import Secret
from sends.github.issue import Issue
from sends.github.main import inputs, outputs, send


@pytest.fixture
def github_output(tmp_path, monkeypatch):
    path = tmp_path / "outputs.txt"
    monkeypatch.setenv('GITHUB_OUTPUT', str(path))

    return path


@pytest.fixture
def github_output_contains(github_output):
    def contains(expected):
        return f'{expected}\n' in github_output.read_text()

    return contains


def test_all_inputs(monkeypatch):
    monkeypatch.setenv('ISSUE_TOKEN', '토큰')
    monkeypatch.setenv('ISSUE_REPOSITORY', '리포')
    monkeypatch.setenv('ISSUE_TITLE', '타이틀')
    monkeypatch.setenv('ISSUE_CONTENT', '내용')
    monkeypatch.setenv('ISSUE_LABEL', '라벨')

    actual = inputs()

    assert actual.token == '토큰'
    assert actual.repository == '리포'
    assert actual.title == '타이틀'
    assert actual.content == '내용'
    assert actual.label == '라벨'


def test_label_is_optional_input(monkeypatch):
    monkeypatch.setenv('ISSUE_TOKEN', '토큰')
    monkeypatch.setenv('ISSUE_REPOSITORY', '리포')
    monkeypatch.setenv('ISSUE_TITLE', '타이틀')
    monkeypatch.setenv('ISSUE_CONTENT', '내용')

    actual = inputs()

    assert not actual.label


def test_outputs(github_output_contains):
    outputs({'number': '679231'})

    assert github_output_contains('number=679231')


@mock.patch('sends.github.main.create')
def test_send(mock_create, github_output_contains):
    mock_create.return_value = {'number': '1'}
    issue = Issue(Secret('token'), 'octocat/example', '제목', '내용', '라벨')

    send(issue)

    mock_create.assert_called_once_with(issue)
    assert github_output_contains('number=1')
