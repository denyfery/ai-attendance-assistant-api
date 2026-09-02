# app/repositories/attendance_repository.py
from sqlalchemy import desc, select
from sqlalchemy.orm import Session
from app.models.attendance_model import Attendance

class AttendanceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, attendance: Attendance) -> Attendance:
        self.db.add(attendance)
        return attendance

    def get_by_id(self, attend_id: str) -> Attendance | None:
        return self.db.execute(
            select(Attendance).where(Attendance.attend_id == attend_id)
        ).scalars().first()

    def get_by_employee(
        self, 
        emp_id: int, 
        limit: int = 20, 
        cursor: str | None = None
    ) -> tuple[list[Attendance], str | None, bool]:
        
        # Query dasar berdasarkan emp_id, diurutkan dari yang terbaru (created_date menurun)
        stmt = select(Attendance).where(Attendance.emp_id == emp_id).order_by(desc(Attendance.created_date))
        
        # Jika cursor ada (biasanya berupa string attend_id atau timestamp), kita ambil data setelah cursor tersebut
        if cursor:
            # Menggunakan attend_id sebagai cursor pembanding
            cursor_record = self.get_by_id(cursor)
            if cursor_record:
                stmt = stmt.where(Attendance.created_date < cursor_record.created_date)

        # Ambil data sejumlah limit + 1 (untuk mengecek apakah masih ada halaman selanjutnya)
        stmt = stmt.limit(limit + 1)
        result = self.db.execute(stmt).scalars().all()

        has_more = False
        if len(result) > limit:
            has_more = True
            result = result[:limit]  # Potong kelebihan datanya

        next_cursor = result[-1].attend_id if has_more and result else None

        return result, next_cursor, has_more

    def get_by_employee_and_date(self, emp_id: int, target_date) -> Attendance | None:
        from sqlalchemy import func
        stmt = select(Attendance).where(
            Attendance.emp_id == emp_id,
            func.date(Attendance.starttime) == target_date,
        )
        result = self.db.execute(stmt)
        return result.scalars().first()