import miro
from . import base


class Picture(base.MiroObject):
    def __init__(self, data: dict, parent):
        super().__init__(data.get("id").lstrip("Optional[").rstrip("]"), parent.client, base.MiroObjectType.PICTURE)
        self.parent = parent
        self.url = data.get("imageUrl")

    def __repr__(self):
        attrs = ("id", "url")
        resolved = [f"{attr}={getattr(self, attr)}" for attr in attrs]
        return f"<Picture {' '.join(resolved)}>"