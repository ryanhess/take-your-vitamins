from fastapi import HTTPException


class ResourceNotFound(HTTPException):
    def __init__(self, msg: str):
        super().__init__(status_code=404, detail=msg)
