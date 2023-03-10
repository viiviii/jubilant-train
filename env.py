import os

from lotto.account import Account
from sends.auth import Auth

ACCOUNT = Account(id_=os.getenv('LOTTERY_ACCOUNT_ID'), password=os.getenv('LOTTERY_ACCOUNT_PASSWORD'))

AUTH = Auth(token=os.getenv('SEND_GITHUB_TOKEN'),
            owner=os.getenv('SEND_GITHUB_OWNER'),
            repository=os.getenv('SEND_GITHUB_REPOSITORY'))
