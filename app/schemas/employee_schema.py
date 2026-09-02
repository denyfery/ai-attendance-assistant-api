from decimal import Decimal
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Generic, TypeVar

T = TypeVar("T")

class EmployeeCreate(BaseModel):
    name: str
    department: str
    salary: Decimal
    phone_number: str | None = None

class EmployeeUpdate(BaseModel):
    name: str | None = None
    department: str | None = None
    salary: Decimal | None = None
    phone_number: str | None = None


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
    department: str
    salary: Decimal
    phone_number: str | None = None

    @field_validator("department", mode="before")
    @classmethod
    def serialize_department(cls, value):
        if hasattr(value, "name"):
            return value.name

        return value


class MessageResponse(BaseModel):
    message: str


class PaginationResponse(
    BaseModel,
    Generic[T]
):
    data: list[T]
    next_cursor: int | None = None
    has_more: bool


class EmployeePaginationResponse(
    PaginationResponse[EmployeeResponse]
):
    pass