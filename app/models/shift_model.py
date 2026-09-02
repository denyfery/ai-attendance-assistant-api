# app/models/shift_model.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, SmallInteger
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.base import Base

class ShiftDaily(Base):
    __tablename__ = "ttamshiftdaily"

    shiftdailycode = Column(String(50), primary_key=True)
    
    # 🛠️ PERBAIKAN: Hapus fsp=3, cukup DateTime saja
    starttime = Column(DateTime)
    endtime = Column(DateTime)
    
    productivehours = Column(Integer, nullable=False)
    daytype = Column(String(5), nullable=False)
    remark = Column(String(255))
    color = Column(String(60))
    is_active = Column(SmallInteger, nullable=False, default=1)
    
    created_by = Column(String(50), nullable=False)
    created_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    modified_by = Column(String(50), nullable=False)
    modified_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    employee_shifts = relationship("EmpShift", back_populates="shift_daily")


class EmpShift(Base):
    __tablename__ = "ttadempshif"

    shiftcode = Column(String(50), primary_key=True)
    emp_id = Column(Integer, ForeignKey("employees.id"), primary_key=True, nullable=False, index=True)
    shiftdailycode = Column(String(50), ForeignKey("ttamshiftdaily.shiftdailycode"), nullable=False)
    
    created_by = Column(String(50), nullable=False)
    created_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    modified_by = Column(String(50), nullable=False)
    modified_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    employee = relationship("Employee")
    shift_daily = relationship("ShiftDaily", back_populates="employee_shifts")