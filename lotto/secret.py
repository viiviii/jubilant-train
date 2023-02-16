class Secret:

    def __init__(self, value: str):
        self._value = value

    def __str__(self) -> str:
        return '*' * len(self._value) if self._value else ''

    def __repr__(self) -> str:
        return f'Secret({self})'

    def __eq__(self, o: object) -> bool:
        return self._value == o

    @property
    def value(self):
        return self._value
