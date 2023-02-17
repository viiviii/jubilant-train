from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


class SendError(Exception):
    def __init__(self, reason: str, detail: str):
        super().__init__(f'[{reason}] {detail}')


@dataclass(frozen=True)
class SendResult:
    title: str
    content: str


class Send(metaclass=ABCMeta):

    @abstractmethod
    def __call__(self, title: str, content: str) -> SendResult:
        pass
