# app/dependencies/attendance_dependency.py
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.employee_repository import EmployeeRepository
from app.services.attendance_service import AttendanceService


def get_attendance_service(db: Session = Depends(get_db)):
    attendance_repo = AttendanceRepository(db)
    employee_repo = EmployeeRepository(db)
    return AttendanceService(
        attendance_repo=attendance_repo, 
        employee_repo=employee_repo, 
        db=db
    )