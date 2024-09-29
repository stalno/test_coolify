from pydantic import BaseModel


class BaseDoc(BaseModel):
    message: str


class UnAuthorizedError(BaseDoc):
    pass


class NotFoundError(BaseDoc):
    pass


class ForbiddenError(BaseDoc):
    pass


class BadRequest(BaseDoc):
    pass


