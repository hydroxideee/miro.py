from typing import Type
from enum import Enum


class MiroObjectType(str,Enum):
    TEAM = "team"
    BOARD = "board"
    WIDGET = "widget"
    USER = "user"
    PICTURE = "picture"

    def __repr__(self) -> str:
        return self.value


class MiroObject:
    def __init__(self,object_id: int | str, client, object_type: MiroObjectType):
        self.id = int(object_id)
        self.type = object_type
        self.client = client

    def __eq__(self, other):
        return self.type == other.type and self.id == other.id
