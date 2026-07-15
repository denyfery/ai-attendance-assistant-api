from data import employees
from fastapi import HTTPException

class EmployeeService:
    def get_all(self):
        return employees

    def get_employee(self, employee_id):        
        for employee in employees:
            if employee["id"] == employee_id:
                return employee
            
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )
            
    def create(self, employee):
        if any(
            emp["name"].lower() == employee.name.lower() and
            emp["department"].lower() == employee.department.lower()
            for emp in employees):
            raise HTTPException(
                status_code=409,
                detail="Employee with this Data already exists"
            )
        
        if employee:
            new_id = max(emp["id"] for emp in employees) + 1 
        else:
            new_id = 1

        new_employee = {
            "id" : new_id,
            "name" : employee.name,
            "department" : employee.department
        }
        
        employees.append(new_employee)
        return employee

    def update(self, employee_id, employee):
        for index, emp in enumerate(employees):
            if emp["id"] == employee_id:
                # hanya ambil field yang tidak None
                update_data = employee.model_dump(exclude_unset=True)
                employees[index].update(update_data)
                
                return employees[index]
        
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    def delete(self, employee_id):
        for index, emp in enumerate(employees):
            if emp["id"] == employee_id:
                del employees[index]
                return True
            
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

def get_employee_service():
    return EmployeeService()