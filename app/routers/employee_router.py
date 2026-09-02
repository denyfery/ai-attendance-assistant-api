from fastapi import APIRouter, Depends

from app.dependencies.employee_dependency import (
    get_employee_service
)

from app.schemas.employee_schema import (
    EmployeeCreate,
    EmployeePaginationResponse,
    EmployeeResponse,
    EmployeeUpdate,
    MessageResponse,
)

from app.services.employee_service import (
    EmployeeService
)

from app.schemas.query_schema import EmployeeFilterParams

# app/routers/employee_router.py
from app.dependencies.auth_dependency import get_current_user, RoleChecker
from app.models.user_model import User # Untuk typing

# 1. Definisikan Level Akses
allow_admin_and_hr = RoleChecker(["admin", "hr"])
allow_admin_only = RoleChecker(["admin"])

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


employee_service_dependency = Depends(
    get_employee_service
)


@router.get(
    "/",
    response_model=EmployeePaginationResponse
)
def get_employees(
    filters: EmployeeFilterParams = Depends(), # <-- FastAPI otomatis mengubah ini jadi Query Params!
    limit: int = 20,
    cursor: int | None = None,
    service: EmployeeService = employee_service_dependency,
    current_user: User = Depends(allow_admin_and_hr) # 🔒 GEMBOK DIPASANG DI SINI
):
    return service.get_all(
        filters=filters,
        limit=limit,
        cursor=cursor
    )


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def get_employee(
    employee_id: int,
    service: EmployeeService = employee_service_dependency,
    current_user: User = Depends(allow_admin_only) # 🔒 GEMBOK DIPASANG DI SINI
):
    return service.get_employee(
        employee_id
    )


@router.post(
    "/",
    response_model=EmployeeResponse
)
def create_employee(
    employee: EmployeeCreate,
    service: EmployeeService = employee_service_dependency,
    current_user: User = Depends(allow_admin_only) # 🔒 GEMBOK DIPASANG DI SINI
):
    return service.create(
        employee
    )


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def update_employee(
    employee_id: int,
    employee_update: EmployeeUpdate,
    service: EmployeeService = employee_service_dependency,
    current_user: User = Depends(allow_admin_only) # 🔒 GEMBOK DIPASANG DI SINI
):
    return service.update(
        employee_id,
        employee_update
    )

@router.delete(
    "/{employee_id}",
    response_model=MessageResponse
)
def delete_employee(
    employee_id: int,
    service: EmployeeService = employee_service_dependency,
    current_user: User = Depends(allow_admin_only) # 🔒 GEMBOK DIPASANG DI SINI
):
    service.delete(
        employee_id
    )

    return {
        "message": "Employee deleted"
    }