import miro
from . import base

class Picture(base.MiroObject):
    def __init__(self, data: dict, parent):
        super().__init__(data.get("id").lstrip("Optional[").rstrip("]"), parent.client, base.MiroObjectType.PICTURE)
        self.parent = parent
        self.url = data.get("imageUrl")