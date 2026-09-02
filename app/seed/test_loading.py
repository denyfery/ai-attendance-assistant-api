from sqlalchemy import select

from app.database.connection import SessionLocal
from app.models.employee_model import Employee
from app.repositories.employee_repository import EmployeeRepository


db = SessionLocal()

try:
    repository = EmployeeRepository(db)

    print("\n=== LAZY ===")

    employees = repository.get_all_lazy()

    for employee in employees:
        print(
            employee.name,
            "->",
            employee.department.name
        )


    print("\n=== JOINEDLOAD ===")

    employees = repository.get_all_joinedload()

    for employee in employees:
        print(
            employee.name,
            "->",
            employee.department.name
        )


    print("\n=== SELECTINLOAD ===")

    employees = repository.get_all_selectinload()

    for employee in employees:
        print(
            employee.name,
            "->",
            employee.department.name
        )

finally:
    db.close()


# Result:

# === LAZY ===
# 2026-08-10 14:00:19,541 INFO sqlalchemy.engine.Engine SELECT DATABASE()
# 2026-08-10 14:00:19,541 INFO sqlalchemy.engine.Engine [raw sql] {}
# 2026-08-10 14:00:19,542 INFO sqlalchemy.engine.Engine SELECT @@sql_mode
# 2026-08-10 14:00:19,542 INFO sqlalchemy.engine.Engine [raw sql] {}
# 2026-08-10 14:00:19,543 INFO sqlalchemy.engine.Engine SELECT @@lower_case_table_names
# 2026-08-10 14:00:19,543 INFO sqlalchemy.engine.Engine [raw sql] {}
# 2026-08-10 14:00:19,544 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2026-08-10 14:00:19,548 INFO sqlalchemy.engine.Engine SELECT employees.id, employees.name, employees.department_id, employees.salary, employees.phone_number 
# FROM employees
# 2026-08-10 14:00:19,548 INFO sqlalchemy.engine.Engine [generated in 0.00017s] {}
# 2026-08-10 14:00:19,552 INFO sqlalchemy.engine.Engine SELECT departments.id AS departments_id, departments.name AS departments_name 
# FROM departments 
# WHERE departments.id = %(pk_1)s
# 2026-08-10 14:00:19,553 INFO sqlalchemy.engine.Engine [generated in 0.00033s] {'pk_1': 1}
# Deny -> Implement
# 2026-08-10 14:00:19,554 INFO sqlalchemy.engine.Engine SELECT departments.id AS departments_id, departments.name AS departments_name 
# FROM departments 
# WHERE departments.id = %(pk_1)s
# 2026-08-10 14:00:19,554 INFO sqlalchemy.engine.Engine [cached since 0.001998s ago] {'pk_1': 2}
# Eka -> Finance
# Fery -> Implement

# === JOINEDLOAD ===
# 2026-08-10 14:00:19,558 INFO sqlalchemy.engine.Engine SELECT employees.id, employees.name, employees.department_id, employees.salary, employees.phone_number, departments_1.id AS id_1, departments_1.name AS name_1 
# FROM employees LEFT OUTER JOIN departments AS departments_1 ON departments_1.id = employees.department_id
# 2026-08-10 14:00:19,559 INFO sqlalchemy.engine.Engine [generated in 0.00027s] {}
# Deny -> Implement
# Eka -> Finance
# Fery -> Implement

# === SELECTINLOAD ===
# 2026-08-10 14:00:19,562 INFO sqlalchemy.engine.Engine SELECT employees.id, employees.name, employees.department_id, employees.salary, employees.phone_number 
# FROM employees
# 2026-08-10 14:00:19,562 INFO sqlalchemy.engine.Engine [generated in 0.00016s] {}
# 2026-08-10 14:00:19,564 INFO sqlalchemy.engine.Engine SELECT departments.id AS departments_id, departments.name AS departments_name 
# FROM departments 
# WHERE departments.id IN (%(primary_keys_1)s, %(primary_keys_2)s)
# 2026-08-10 14:00:19,565 INFO sqlalchemy.engine.Engine [generated in 0.00031s] {'primary_keys_1': 1, 'primary_keys_2': 2}
# Deny -> Implement
# Eka -> Finance
# Fery -> Implement
# 2026-08-10 14:00:19,570 INFO sqlalchemy.engine.Engine ROLLBACK