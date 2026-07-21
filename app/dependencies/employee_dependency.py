from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.repositories.employee_repository import EmployeeRepository
from app.services.employee_service import EmployeeService


def get_employee_service(
    db: Session = Depends(get_db)
):
    repository = EmployeeRepository(db)
    return EmployeeService(
        repository,
        db
    )