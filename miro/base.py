from . import enums


class MiroObject:
    def __init__(self,object_id: int | str, client, object_type: enums.MiroObjectType):
        try:
            self.id = int(object_id)
        except ValueError:
            self.id = str(object_id)
        self.type = object_type
        self.client = client

    def __eq__(self, other):
        return self.type == other.type and self.id == other.id
