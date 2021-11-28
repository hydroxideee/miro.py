import miro
import io
import requests
from . import base


class Picture(base.MiroObject):
    def __init__(self, data: dict, parent):
        super().__init__(data.get("id").lstrip("Optional[").rstrip("]"), parent.client, base.MiroObjectType.PICTURE)
        self.parent = parent
        self.url = data.get("imageUrl")

    def save(self, fp, seek_start=True):
        response = requests.get(self.url)
        if not response.ok:
            raise miro.HTTPException(response)
        data = response.content
        if isinstance(fp, io.IOBase) and fp.writable():
            written = fp.write(data)
            if seek_start:
                fp.seek(0)
            return written
        else:
            with open(fp, 'wb') as f:
                return f.write(data)

    def __repr__(self):
        attrs = ("id", "url")
        resolved = [f"{attr}={getattr(self, attr)}" for attr in attrs]
        return f"<Picture {' '.join(resolved)}>"
