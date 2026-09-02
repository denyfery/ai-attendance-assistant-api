from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.employee_model import Employee
from app.models.department_model import Department


db: Session = SessionLocal()

try:
    stmt = (
        select(
            Employee.id,
            Employee.name,
            Department.name.label("department_name")
        )
        .join(
            Department,
            Employee.department_id == Department.id
        )
    )

    result = db.execute(stmt)

    for row in result:
        print(
            f"ID: {row.id} | "
            f"Name: {row.name} | "
            f"Department: {row.department_name}"
        )

finally:
    db.close()