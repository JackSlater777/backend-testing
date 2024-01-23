from dataclasses import dataclass, field
from framework.enums.enums import StringableEnum


class Type(StringableEnum):
    Type_one = "Type_one"
    Type_two = "Type_two"


@dataclass
class Message:
    ids: list = field(default_factory=list)
    type: Type = None
    message_id: str = None
    additional_info: dict = field(default_factory=dict)

    def __hash__(self):
        return hash(self.message_id)
