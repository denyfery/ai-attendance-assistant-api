from sqlalchemy.orm import Session
from app.models.employee_model import Employee
from sqlalchemy import select

class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        stmt = select(Employee)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_by_id(self,employee_id):
        stmt = select(Employee).where(Employee.id == employee_id)
        result = self.db.execute(stmt)
        return result.scalars().one_or_none()

    def create(self,employee: Employee):        
        self.db.add(employee)
        return employee
    
    # def update(self, employee_id, employee_data):
    #     employee = self.get_by_id(employee_id)
    #     if employee is None:
    #         return None

    #     employee.name = employee_data.name
    #     employee.department = employee_data.department
    #     employee.salary = employee_data.salary

    #     return employee

    def delete(self, employee: Employee):
        self.db.delete(employee)
    
    def exists_by_name_department(
        self,
        name,
        department
    ):
        stmt = select(Employee).where(
        Employee.name == name,
        Employee.department == department
        )
        return self.db.execute(stmt).scalar_one_or_none()
