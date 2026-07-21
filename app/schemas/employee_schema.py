from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Optional

class Employee(BaseModel):
    id: int
    name: str
    department: str
    salary:Decimal

class EmployeeCreate(BaseModel):
    name: str
    department: str
    salary: Decimal

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    salary: Optional[Decimal] = None

class EmployeeDelete(BaseModel):
    id: int

class EmployeeResponse(BaseModel):
    id: int
    name: str
    department: str
    salary:Decimal = Field(..., max_digits=15, decimal_places=2)

class MessageResponse(BaseModel):
    message: str