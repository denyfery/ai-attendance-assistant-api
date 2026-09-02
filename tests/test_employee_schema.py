from decimal import Decimal

from app.models.department_model import Department
from app.models.employee_model import Employee
from app.schemas.employee_schema import EmployeeResponse


def test_employee_response_converts_department_model_to_name():
    department = Department(name="Engineering")
    employee = Employee(
        name="Alice",
        department=department,
        salary=Decimal("1000.00"),
        phone_number="1234567890",
    )
    employee.id = 1

    response = EmployeeResponse.model_validate(employee)

    assert response.department == "Engineering"
