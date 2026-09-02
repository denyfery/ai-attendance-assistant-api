# app/models/attendance_model.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database.base import Base

class Attendance(Base):
    __tablename__ = "TTADATTENDANCE"

    # Primary Key
    attend_id = Column(String(150), primary_key=True)
    
    # Foreign Key ke employees (Disamakan jadi Integer)
    emp_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    
    # Waktu Shift & Aktual
    shiftstarttime = Column(DateTime, index=True)
    shiftendtime = Column(DateTime, index=True)
    starttime = Column(DateTime)
    endtime = Column(DateTime)
    
    # Kalkulasi Menit/Waktu
    actual_in = Column(Integer)
    actual_out = Column(Integer)
    actualworkmnt = Column(Integer)
    
    # Status & Tipe Hari
    daytype = Column(String(5), nullable=False)
    attend_code = Column(String(50)) # 🆕 "present", "late", "absent", "leave"
    remark = Column(String(5000))
    
    # Overtime (Lembur)
    total_ot = Column(Float)
    total_otindex = Column(Float)
    
    # Validasi Anti-Fraud (Lokasi, IP, Foto)
    ip_starttime = Column(String(20))
    ip_endtime = Column(String(20))
    photo_start = Column(String(255))
    photo_end = Column(String(255))
    geoloc_start = Column(String(255))
    geoloc_end = Column(String(255))
    
    # Audit Trail
    created_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    created_by = Column(String(50), nullable=False)
    modified_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    modified_by = Column(String(50), nullable=False)

    # Relationship ke Employee
    employee = relationship("Employee", back_populates="attendances")