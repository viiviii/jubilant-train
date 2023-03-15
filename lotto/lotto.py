from abc import ABCMeta, abstractmethod

from lotto.account import Account
from lotto.types import DateRange, Table


class Lotto(metaclass=ABCMeta):

    @abstractmethod
    def login(self, account: Account) -> None:
        pass

    @abstractmethod
    def buy(self, amount: int) -> int:
        pass

    @abstractmethod
    def result(self, dates: DateRange) -> Table:
        pass


class LottoError(Exception):
    def __init__(self, reason: str, detail: str):
        super().__init__(f'[{reason}] {detail}')
