import pytest


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


@pytest.fixture
def assert_contains_multiline_github_output(github_output):
    def assertions(name, value):
        assert f'{name}<<' in github_output.read_text()
        assert value in github_output.read_text()

    return assertions
