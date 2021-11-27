from typing import TYPE_CHECKING

from requests import Response

__all__ = (
    'MiroException',
    'HTTPException'
)



class MiroException(Exception):
    """Base exception class for miro.py
    """
    pass


class HTTPException(MiroException):
    """Exception raised when an HTTP request fails
    """
    def __init__(self, response: Response):
        self.response: Response = response
        self.status_code: int = response.status_code
        self.data: dict = response.json()
        self.code: str = self.data.get("code")
        self.message: str = self.data.get("message")
        fms = "{0.status_code} {0.reason} (error code: {1}) : {2}"
        super().__init__(fms.format(self.response,self.code,self.message))

class ObjectException(MiroException):
    def __init__(self,object_data: dict):
        super().__init__()