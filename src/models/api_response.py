from typing import List

from pydantic import BaseModel, ValidationError
from pydantic_core import ErrorDetails


class ErrorMessage(BaseModel):
    code: str
    message: str

    @classmethod
    def fromdetail(cls, error: ErrorDetails):
        code = error["type"]
        if error["loc"]:
            message = f"{error['loc'][0]}. {error['msg']}"
        else:
            message = error["msg"]

        return cls(code=code, message=message)


class ValidationResponse(BaseModel):
    valid: bool
    errors: List[ErrorMessage] | None = None

    @classmethod
    def fromerrors(cls, errors: ValidationError):
        return cls(valid=False, errors=[ErrorMessage.fromdetail(detail) for detail in errors.errors()])
