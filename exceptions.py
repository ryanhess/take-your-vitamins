from fastapi import HTTPException


class ResourceNotFound(HTTPException):
    def __init__(self, resource_type: type, resource_ids: int | list[int]):
        super().__init__(
            status_code=404, detail=f"{resource_type.__name__} {resource_ids} not found"
        )
