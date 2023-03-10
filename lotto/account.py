from lotto.secret import Secret


class Account:
    def __init__(self, id_: str, password: str) -> None:
        self._id = id_
        self._secret = Secret(password)

        if not id_ or not password:
            raise ValueError(f'계정 정보는 필수 값 입니다. {self.__repr__()}')

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
