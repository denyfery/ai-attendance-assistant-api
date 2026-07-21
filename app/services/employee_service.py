from app.data.employee_data import employees
from fastapi import HTTPException
from app.models.employee_model import Employee
from app.repositories.employee_repository import EmployeeRepository
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.schemas.employee_schema import EmployeeCreate


class AppException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class DuplicateEmployeeException(AppException):
    def __init__(self, message: str = "Employee already exists"):
        super().__init__(message)


class EmployeeNotFoundException(AppException):
    def __init__(self, message: str = "Employee not found"):
        super().__init__(message)


class EmployeeService:
    def __init__(self, repository: EmployeeRepository, db: Session):
        self.db = db
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_employee(self, employee_id):
        emp = self.repository.get_by_id(employee_id)
        if emp is None:
            raise EmployeeNotFoundException()

        return emp
        # for employee in employees:
        #     if employee["id"] == employee_id:
        #         return employee
            
        # raise HTTPException(
        #     status_code=404,
        #     detail="Employee not found"
        # )
            
    def create(self, employee: EmployeeCreate) -> Employee:
        existing_emp = self.repository.exists_by_name_department(
            employee.name,
            employee.department,
        )

        if existing_emp is not None:
            raise DuplicateEmployeeException()

        new_employee = Employee(
            name=employee.name,
            department=employee.department,
            salary=employee.salary,
        )

        try:
            created = self.repository.create(new_employee)
            self.db.commit()
            self.db.refresh(created)
            return created

        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Database error occurred: {str(e)}",
            ) from e

        # employees.append(new_employee)
        # return employee

    def update(self, employee_id, employee_update):
        employee = self.repository.get_by_id(employee_id)

        if employee is None:
            raise EmployeeNotFoundException()

        update_data = employee_update.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in update_data.items():
            setattr(employee, key, value)

        self.db.commit()
        self.db.refresh(employee)

        return employee
        # for index, emp in enumerate(employees):
        #     if emp["id"] == employee_id:
        #         # hanya ambil field yang tidak None
        #         update_data = employee.model_dump(exclude_unset=True)
        #         employees[index].update(update_data)
                
        #         return employees[index]
        
        # raise HTTPException(
        #     status_code=404,
        #     detail="Employee not found"
        # )

    def delete(self, employee_id):
        employee = self.repository.get_by_id(employee_id)

        if employee is None:
            raise EmployeeNotFoundException()

        self.repository.delete(employee)
        self.db.commit()

        # for index, emp in enumerate(employees):
        #     if emp["id"] == employee_id:
        #         del employees[index]
        #         return True
            
        # raise HTTPException(
        #     status_code=404,
        #     detail="Employee not found"
        # )