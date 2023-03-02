from abc import ABCMeta, abstractmethod
from typing import List

from lotto.types import DateRange


class Account(object):
    def __init__(self, account_id: str, account_password: str) -> None:
        self.id = account_id
        self.password = account_password

    def __str__(self) -> str:
        def mask(string) -> str:
            return '*' * len(string)

        return f'id={self.id}, ' \
               f'password={mask(self.password) if self.password else self.password}'

    def __repr__(self) -> str:
        return f'Account({self})'


class Lotto(metaclass=ABCMeta):

    @abstractmethod
    def login(self, account: Account) -> None:
        pass

    @abstractmethod
    def buy(self, amount: int) -> int:
        pass

    @abstractmethod
    def result(self, dates: DateRange) -> List[dict[str, str]]:
        pass


class LottoError(Exception):
    def __init__(self, reason: str, detail: str):
        super().__init__(f'[{reason}] {detail}')
