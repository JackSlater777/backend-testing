from enum import Enum


class StringableEnum(Enum):
    def __str__(self):
        return self._name_


class StrValueEnum(Enum):
    def str(self) -> str:
        return self.value
