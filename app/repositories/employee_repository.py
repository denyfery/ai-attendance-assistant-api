from sqlalchemy import select, asc, desc, exists
from sqlalchemy.orm import (
    joinedload,
    Session
)

from app.models.employee_model import Employee
from app.models.department_model import Department
from app.schemas.query_schema import EmployeeFilterParams


class EmployeeRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        filters: EmployeeFilterParams, # <-- Gunakan class yang baru kita buat
        cursor: int | None = None,
        limit: int = 20
    ):
        # 1. Base Query + Eager Loading
        stmt = select(Employee).options(joinedload(Employee.department))

        # 2. DYNAMIC FILTERING (Pasang Lego satu-satu)
        if filters.department:
            stmt = stmt.join(Employee.department).where(Department.name == filters.department)
        
        if filters.name:
            # Menggunakan ilike untuk pencarian case-insensitive (misal: "budi" akan match "Budi")
            stmt = stmt.where(Employee.name.ilike(f"%{filters.name}%"))
            
        if filters.min_salary:
            stmt = stmt.where(Employee.salary >= filters.min_salary)

        # 3. CURSOR PAGINATION
        if cursor is not None:
            stmt = stmt.where(Employee.id > cursor)

        # 4. DYNAMIC SORTING
        # Hati-hati: Sorting non-ID dengan Cursor Pagination butuh logic tambahan.
        # Untuk sekarang kita aplikasikan basic dynamic sorting.
        sort_column = getattr(Employee, filters.sort_by, Employee.id)
        
        if filters.sort_order.lower() == "desc":
            stmt = stmt.order_by(desc(sort_column))
        else:
            stmt = stmt.order_by(asc(sort_column))

        # 5. LIMIT
        stmt = stmt.limit(limit + 1)

        result = self.db.execute(stmt)
        employees = result.scalars().all()

        has_more = len(employees) > limit
        employees = employees[:limit]

        next_cursor = employees[-1].id if has_more and employees else None

        return employees, next_cursor, has_more

    def get_by_id(
        self,
        employee_id: int
    ):
        stmt = (
            select(Employee)
            .options(
                joinedload(Employee.department)
            )
            .where(
                Employee.id == employee_id
            )
        )

        result = self.db.execute(stmt)

        return result.scalars().one_or_none()

    def get_department_by_name(
        self,
        department_name: str
    ):
        stmt = (
            select(Department)
            .where(
                Department.name == department_name
            )
        )

        result = self.db.execute(stmt)

        return result.scalars().one_or_none()

    def exists_by_name_department(
        self,
        name: str,
        department_name: str
    ):
        stmt = (
            select(
                exists().where(
                    Employee.name == name,
                    Employee.department.has(
                        Department.name == department_name
                    )
                )
            )
        )

        return self.db.execute(stmt).scalar()

    def create(
        self,
        employee: Employee
    ):
        self.db.add(employee)

        return employee

    # def update(
    #     self,
    #     employee: Employee,
    #     employee_data
    # ):
    #     update_data = employee_data.model_dump(
    #         exclude_unset=True,
    #         exclude_none=True
    #     )

    #     for key, value in update_data.items():
    #         setattr(employee, key, value)

    #     return employee
    # ❌ FUNGSI UPDATE handle di service ❌

    def delete(
        self,
        employee: Employee
    ):
        self.db.delete(employee)