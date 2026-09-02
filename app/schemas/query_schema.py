from fastapi import Query

class EmployeeFilterParams:
    def __init__(
        self,
        department: str | None = Query(None, description="Filter by department name"),
        name: str | None = Query(None, description="Search by employee name"),
        min_salary: int | None = Query(None, description="Minimum salary"),
        sort_by: str = Query("id", description="Column to sort by (id, name, salary)"),
        sort_order: str = Query("asc", description="Sort direction (asc or desc)")
    ):
        self.department = department
        self.name = name
        self.min_salary = min_salary
        self.sort_by = sort_by
        self.sort_order = sort_order