from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.employee_model import Employee
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee_schema import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,
    EmployeePaginationResponse,
)
from app.schemas.query_schema import EmployeeFilterParams

class AppException(Exception):

    def __init__(
        self,
        message: str
    ):
        self.message = message
        super().__init__(message)


class DuplicateEmployeeException(AppException):

    def __init__(
        self,
        message: str = "Employee already exists"
    ):
        super().__init__(message)


class EmployeeNotFoundException(AppException):

    def __init__(
        self,
        message: str = "Employee not found"
    ):
        super().__init__(message)


class DepartmentNotFoundException(AppException):

    def __init__(
        self,
        message: str = "Department not found"
    ):
        super().__init__(message)


class DatabaseException(AppException):

    def __init__(
        self,
        message: str = "Database error occurred"
    ):
        super().__init__(message)


class EmployeeService:

    def __init__(
        self,
        repository: EmployeeRepository,
        db: Session
    ):
        self.repository = repository
        self.db = db

    def get_all(
        self,
        filters: EmployeeFilterParams, # <-- Update tipe datanya
        cursor: int | None = None,
        limit: int = 20
    ) -> EmployeePaginationResponse:

        employees, next_cursor, has_more = (
            self.repository.get_all(
                filters=filters, # <-- Oper object filternya langsung
                cursor=cursor,
                limit=limit
            )
        )

        return EmployeePaginationResponse(
            data=[
                EmployeeResponse.model_validate(
                    employee
                )
                for employee in employees
            ],
            next_cursor=next_cursor,
            has_more=has_more
        )

    def get_employee(
        self,
        employee_id: int
    ) -> EmployeeResponse:

        employee = self.repository.get_by_id(
            employee_id
        )

        if employee is None:
            raise EmployeeNotFoundException()

        return EmployeeResponse.model_validate(
            employee
        )

    def create(
        self,
        employee: EmployeeCreate
    ) -> EmployeeResponse:

        # 1. Check duplicate employee
        existing_employee = (
            self.repository.exists_by_name_department(
                employee.name,
                employee.department
            )
        )

        if existing_employee:
            raise DuplicateEmployeeException()

        # 2. Find department
        department = (
            self.repository.get_department_by_name(
                employee.department
            )
        )

        if department is None:
            raise DepartmentNotFoundException(
                f"Department '{employee.department}' not found"
            )

        # 3. Create ORM object
        new_employee = Employee(
            name=employee.name,
            department=department,
            salary=employee.salary,
            phone_number=employee.phone_number
        )

        try:

            # 4. Add object to session
            created = self.repository.create(
                new_employee
            )

            # 5. Commit transaction
            self.db.commit()

            # 6. Refresh object
            self.db.refresh(created)

            # 7. Return response
            return EmployeeResponse.model_validate(
                created
            )

        except SQLAlchemyError as e:

            self.db.rollback()

            raise DatabaseException(
                "Failed to create employee"
            ) from e

    def update(
        self,
        employee_id: int,
        employee_update: EmployeeUpdate
    ) -> EmployeeResponse:

        # 1. Find employee
        employee = self.repository.get_by_id(
            employee_id
        )

        if employee is None:
            raise EmployeeNotFoundException()

        try:

            # 2. Convert schema to dictionary
            update_data = employee_update.model_dump(
                exclude_unset=True,
                exclude_none=True
            )

            # --- TAMBAHKAN LOGIKA INI ---
            if "department" in update_data:
                dept_name = update_data.pop("department")
                department = self.repository.get_department_by_name(dept_name)
                
                if department is None:
                    raise DepartmentNotFoundException(f"Department '{dept_name}' not found")
                
                employee.department = department
            # ----------------------------

            # 3. Update ORM entity
            for key, value in update_data.items():
                setattr(
                    employee,
                    key,
                    value
                )

            # 4. Commit transaction
            self.db.commit()

            # 5. Refresh object
            self.db.refresh(employee)

            # 6. Return response
            return EmployeeResponse.model_validate(
                employee
            )

        except SQLAlchemyError as e:

            self.db.rollback()

            raise DatabaseException(
                "Failed to update employee"
            ) from e

    def delete(
        self,
        employee_id: int
    ) -> None:

        # 1. Find employee
        employee = self.repository.get_by_id(
            employee_id
        )

        if employee is None:
            raise EmployeeNotFoundException()

        try:

            # 2. Delete employee
            self.repository.delete(
                employee
            )

            # 3. Commit transaction
            self.db.commit()

        except SQLAlchemyError as e:

            self.db.rollback()

            raise DatabaseException(
                "Failed to delete employee"
            ) from e