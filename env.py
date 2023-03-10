import os

from lotto.account import Account
from sends.github import Github

ACCOUNT = Account(id_=os.getenv('LOTTERY_ACCOUNT_ID'), password=os.getenv('LOTTERY_ACCOUNT_PASSWORD'))

GITHUB = Github(token=os.getenv('SEND_GITHUB_TOKEN'), repository=os.getenv('SEND_GITHUB_REPOSITORY'))
