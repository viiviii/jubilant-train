from lotto.secret import Secret


class Account:
    def __init__(self, id_: str, password: str) -> None:
        self._id = id_
        self._secret = Secret(password)

    @property
    def id(self):
        return self._id

    @property
    def password(self):
        return self._secret.value

    def __str__(self) -> str:
        return f'id={self._id}, password={self._secret}'

    def __repr__(self) -> str:
        return f'Account({self})'
