from fastapi import APIRouter
from fastapi import Depends

from app.schemas.employee_schema import EmployeeCreate
from app.schemas.employee_schema import EmployeeUpdate

from app.services.employee_service import EmployeeService

from app.dependencies.employee_dependency import get_employee_service

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)

@router.get("/")
def get_all(
    service: EmployeeService = Depends(get_employee_service)
):
    return service.get_all()

@router.get("/{employee_id}")
def get_employee(
    employee_id: int,
    service: EmployeeService = Depends(get_employee_service)
):
    return service.get_employee(employee_id)

@router.post("/")
def create_employee(
    employee: EmployeeCreate,
    service: EmployeeService = Depends(get_employee_service)
):
    return service.create(employee)

@router.put("/{employee_id}")
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    service: EmployeeService = Depends(get_employee_service)
):
    return service.update(employee_id, employee)

@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    service: EmployeeService = Depends(get_employee_service)
):
    service.delete(employee_id)

    return {
        "message":"Employee deleted"
    }