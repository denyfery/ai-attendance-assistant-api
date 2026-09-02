from sqlalchemy import select

from app.database.connection import SessionLocal
from app.models import Employee, Department


db = SessionLocal()

try:
    stmt = select(Employee)

    result = db.execute(stmt)

    employees = result.scalars().all()

    for employee in employees:
        print(
            employee.name,
            "->",
            employee.department.name
        )

finally:
    db.close()