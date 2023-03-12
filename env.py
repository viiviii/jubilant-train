import os

from lotto.account import Account

ACCOUNT = Account(id_=os.getenv('LOTTERY_ACCOUNT_ID'), password=os.getenv('LOTTERY_ACCOUNT_PASSWORD'))
