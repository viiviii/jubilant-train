import os

from lotto.secret import Secret


class Auth:

    def __init__(self, token: str, owner: str, repository: str) -> None:
        """
        Parameters:
            token (str): A token to authenticate on your repository
            owner (str): The repository owner's username
            repository (str): The owner and repository name

        Example:
            token: ghq_nZn7aQ...
            owner: octocat
            repository: octocat/Hello-World
        """
        self._token = Secret(token)
        self._owner = owner
        self._repository = repository

        if not token or not owner or not repository:
            raise ValueError(f'인증 정보는 필수 값 입니다. {self.__repr__()}')

    @property
    def token(self):
        return self._token.value

    @property
    def owner(self):
        return self._owner

    @property
    def repository(self):
        return self._repository

    def __str__(self) -> str:
        return f'token={self._token}, owner={self.owner}, repository={self.repository}'

    def __repr__(self) -> str:
        return f'Auth({self})'


def from_env() -> Auth:
    return Auth(
        token=os.environ['SEND_GITHUB_TOKEN'],
        owner=os.environ['SEND_GITHUB_OWNER'],
        repository=os.environ['SEND_GITHUB_REPOSITORY']
    )
