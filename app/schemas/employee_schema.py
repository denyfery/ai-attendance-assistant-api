from pydantic import BaseModel
from typing import Optional

class Employee(BaseModel):
    id: int
    name: str
    department: str

class EmployeeCreate(BaseModel):
    name: str
    department: str

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None

class EmployeeDelete(BaseModel):
    id: int