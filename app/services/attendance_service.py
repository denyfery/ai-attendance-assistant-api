# app/services/attendance_service.py
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, func

from app.models.attendance_model import Attendance
from app.models.user_model import User
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.attendance_schema import (
    AttendanceCreate, 
    AttendanceUpdate, 
    AttendanceResponse, 
    AttendancePaginationResponse
)
from app.services.employee_service import DatabaseException, EmployeeNotFoundException

class AttendanceNotFoundException(Exception):
    def __init__(self, message="Attendance record not found"):
        self.message = message
        super().__init__(self.message)


class AttendanceService:
    def __init__(
        self, 
        attendance_repo: AttendanceRepository, 
        employee_repo: EmployeeRepository, 
        db: Session
    ):
        self.attendance_repo = attendance_repo
        self.employee_repo = employee_repo
        self.db = db

    def check_in(
        self, 
        data: AttendanceCreate, 
        current_user: User
    ) -> AttendanceResponse:
        
        # 1. Validasi Karyawan
        employee = self.employee_repo.get_by_id(data.emp_id)
        if not employee:
            raise EmployeeNotFoundException(f"Employee with ID {data.emp_id} not found")

        # 🛡️ 2. VALIDASI ANTI-DOUBLE CHECK-IN: Cek apakah sudah absen di tanggal yang sama
        target_date = data.starttime.date()
        existing_attendance = self.db.execute(
            select(Attendance).where(
                Attendance.emp_id == data.emp_id,
                func.date(Attendance.starttime) == target_date
            )
        ).scalars().first()

        if existing_attendance:
            raise DatabaseException(f"Karyawan dengan ID {data.emp_id} sudah melakukan check-in hari ini.")

        # 3. 🔍 AUTO-FETCH SHIFT
        from app.models.shift_model import EmpShift, ShiftDaily
        
        shift_mapping = self.db.execute(
            select(ShiftDaily)
            .join(EmpShift, EmpShift.shiftdailycode == ShiftDaily.shiftdailycode)
            .where(EmpShift.emp_id == data.emp_id, ShiftDaily.is_active == 1)
        ).scalars().first()

        shift_start_time = None
        shift_end_time = None
        day_type = "WD"
        
        if shift_mapping:
            if shift_mapping.starttime:
                shift_start_time = datetime.combine(target_date, shift_mapping.starttime.time())
            if shift_mapping.endtime:
                shift_end_time = datetime.combine(target_date, shift_mapping.endtime.time())
            day_type = shift_mapping.daytype

        # 4. KELOLA KETERLAMBATAN OTOMATIS
        actual_in_minutes = 0
        attend_code = "present"
        
        if shift_start_time and data.starttime:
            req_starttime = data.starttime.replace(tzinfo=None) if data.starttime.tzinfo else data.starttime
            master_starttime = shift_start_time.replace(tzinfo=None) if shift_start_time.tzinfo else shift_start_time

            delta_seconds = (req_starttime - master_starttime).total_seconds()
            if delta_seconds > 0:
                actual_in_minutes = int(delta_seconds / 60)
                attend_code = "late"

        # 5. Buat Object Attendance
        new_attendance = Attendance(
            attend_id=data.attend_id,
            emp_id=data.emp_id,
            daytype=day_type,
            attend_code=attend_code,
            shiftstarttime=shift_start_time,
            shiftendtime=shift_end_time,
            starttime=data.starttime,
            geoloc_start=data.geoloc_start,
            photo_start=data.photo_start,
            ip_starttime=data.ip_starttime,
            actual_in=actual_in_minutes,
            created_by=current_user.username,
            modified_by=current_user.username
        )

        try:
            created = self.attendance_repo.create(new_attendance)
            self.db.commit()
            self.db.refresh(created)
            return AttendanceResponse.model_validate(created)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseException("Failed to process check-in") from e
        
    def check_out(
        self, 
        attend_id: str, 
        data: AttendanceUpdate, 
        current_user: User
    ) -> AttendanceResponse:
        
        # 1. Cari data absen check-in sebelumnya
        attendance = self.attendance_repo.get_by_id(attend_id)
        if not attendance:
            raise AttendanceNotFoundException()

        # 2. Update data dasar dari schema
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in update_data.items():
            setattr(attendance, key, value)

        # 3. 🧠 THE MAGIC 2: Kalkulasi Durasi Kerja (actualworkmnt & actual_out)
        if attendance.endtime:
            # Normalisasi endtime agar bebas dari konflik timezone
            req_endtime = attendance.endtime.replace(tzinfo=None) if attendance.endtime.tzinfo else attendance.endtime

            if attendance.starttime:
                req_starttime = attendance.starttime.replace(tzinfo=None) if attendance.starttime.tzinfo else attendance.starttime
                work_delta = (req_endtime - req_starttime).total_seconds()
                attendance.actualworkmnt = int(work_delta / 60)

            if attendance.shiftendtime:
                master_endtime = attendance.shiftendtime.replace(tzinfo=None) if attendance.shiftendtime.tzinfo else attendance.shiftendtime
                out_delta = (req_endtime - master_endtime).total_seconds()
                # Jika minus = pulang cepat. Jika plus = lembur.
                attendance.actual_out = int(out_delta / 60)

        # 4. Rekam jejak siapa yang mengubah data (Audit Trail)
        attendance.modified_by = current_user.username
        attendance.modified_date = datetime.now(timezone.utc)

        try:
            self.db.commit()
            self.db.refresh(attendance)
            return AttendanceResponse.model_validate(attendance)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseException("Failed to process check-out") from e
                    
    def get_employee_history(
        self, 
        emp_id: int, 
        limit: int = 20, 
        cursor: str | None = None
    ) -> AttendancePaginationResponse:
        
        if not self.employee_repo.get_by_id(emp_id):
            raise EmployeeNotFoundException()
            
        attendances, next_cursor, has_more = self.attendance_repo.get_by_employee(
            emp_id=emp_id, limit=limit, cursor=cursor
        )
        
        return AttendancePaginationResponse(
            data=[AttendanceResponse.model_validate(a) for a in attendances],
            has_more=has_more,
            next_cursor=next_cursor
        )