from . import enums


class MiroObject:
    def __init__(self,object_id: int | str, client, object_type: enums.MiroObjectType):
        self.id = int(object_id)
        self.type = object_type
        self.client = client

    def __eq__(self, other):
        return self.type == other.type and self.id == other.id
