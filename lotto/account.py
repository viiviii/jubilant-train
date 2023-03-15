from dataclasses import dataclass

from lotto.secret import Secret


@dataclass(frozen=True)
class Account:
    id: str
    password: Secret
