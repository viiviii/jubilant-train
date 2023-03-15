import os
from datetime import datetime, date
from typing import Optional

from lotto.account import Account
from lotto.types import DateRange

LOTTERY_ACCOUNT_ID = 'LOTTERY_ACCOUNT_ID'
LOTTERY_ACCOUNT_PASSWORD = 'LOTTERY_ACCOUNT_PASSWORD'


def to_account() -> Account:
    return Account(
        id_=_required(LOTTERY_ACCOUNT_ID),
        password=_required(LOTTERY_ACCOUNT_PASSWORD),
    )


SEARCH_START_DATE = 'SEARCH_START_DATE'
SEARCH_END_DATE = 'SEARCH_END_DATE'


def to_search_date_range() -> DateRange:
    return DateRange(
        start=_to_date(_optional(SEARCH_START_DATE)) or date.today(),
        end=_to_date(_optional(SEARCH_END_DATE)) or date.today(),
    )


def _required(key: str) -> str:
    return os.environ[key]


def _optional(key: str) -> Optional[str]:
    return os.getenv(key)


def _to_date(string: Optional[str]) -> Optional[date]:
    if not string:
        return None
    return datetime.strptime(string, '%Y-%m-%d').date()
