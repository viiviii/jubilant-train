from argparse import ArgumentParser
from typing import Optional

import keyring

ID_ARGUMENT_NAME = '--id'
ID_ARGUMENT_OPTIONS = {'type': str, 'help': '로또 사이트 계정 아이디'}
KEYRING_SERVICE_NAME = 'lotto-purchase-keyring'


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


def fetch_account() -> Account:
    _id = _id_from_args()
    return Account(_id, _password_from_keyring(_id))


def _id_from_args() -> str:
    parser = ArgumentParser()
    parser.add_argument(ID_ARGUMENT_NAME, **ID_ARGUMENT_OPTIONS)
    known_args = parser.parse_known_args()[0]
    return known_args.id


def _password_from_keyring(account_id: str) -> Optional[str]:
    """ 최초 1회 [system keyring service]에 계정을 등록해야 함.

    등록 방법:
        코드 사용 (등록 후 제거할 것)
        > keyring.set_password(`KEYRING_SERVICE_NAME`, 'id', 'password')

        커맨드 라인 사용
        $ keyring set `KEYRING_SERVICE_NAME` 'id'

    주의:
        이 작업은 현재 등록하는 계정 정보에 python 접근을 허용함.

    기타:
        macOS key chain 사용은 macOS 11, python 3.8.7 이상을 필요로 함.
    """
    return keyring.get_password(KEYRING_SERVICE_NAME, account_id)
