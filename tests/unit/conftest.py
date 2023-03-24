import pytest


@pytest.fixture
def github_output(tmp_path, monkeypatch):
    path = tmp_path / "outputs.txt"
    monkeypatch.setenv('GITHUB_OUTPUT', str(path))

    return path


@pytest.fixture
def assert_contains_github_output(github_output):
    def assertion(name, value):
        assert f'{name}={value}\n' in github_output.read_text()

    return assertion


@pytest.fixture
def assert_contains_multiline_github_output(github_output):
    def assertion(name, value):
        assert f'{name}<<' in github_output.read_text()
        assert value in github_output.read_text()

    return assertion
