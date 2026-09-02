# app/routers/attendance_router.py
from fastapi import APIRouter, Depends

from app.dependencies.attendance_dependency import get_attendance_service
from app.dependencies.auth_dependency import RoleChecker
from app.models.user_model import User
from app.schemas.attendance_schema import (
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceResponse,
    AttendancePaginationResponse
)
from app.services.attendance_service import AttendanceService

router = APIRouter(
    prefix="/attendances",
    tags=["Attendances"]
)

# Definisikan Hak Akses (RBAC)
allow_admin_and_hr = RoleChecker(["admin", "hr"])
allow_admin_only = RoleChecker(["admin"])


@router.post(
    "/check-in", 
    response_model=AttendanceResponse
)
def check_in(
    data: AttendanceCreate,
    service: AttendanceService = Depends(get_attendance_service),
    # 🔒 Bisa diakses Admin & HR (untuk tahap ini)
    current_user: User = Depends(allow_admin_and_hr) 
):
    return service.check_in(data, current_user)


@router.put(
    "/{attend_id}/check-out", 
    response_model=AttendanceResponse
)
def check_out(
    attend_id: str,
    data: AttendanceUpdate,
    service: AttendanceService = Depends(get_attendance_service),
    # 🔒 Bisa diakses Admin & HR
    current_user: User = Depends(allow_admin_and_hr)
):
    return service.check_out(attend_id, data, current_user)


@router.get(
    "/employee/{emp_id}", 
    response_model=AttendancePaginationResponse
)
def get_employee_history(
    emp_id: int,
    limit: int = 20,
    cursor: str | None = None,
    service: AttendanceService = Depends(get_attendance_service),
    current_user: User = Depends(allow_admin_and_hr)
):
    return service.get_employee_history(
        emp_id=emp_id, 
        limit=limit, 
        cursor=cursor
    )