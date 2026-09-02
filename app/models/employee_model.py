from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, DECIMAL
from decimal import Decimal

from app.database.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.department_model import Department

class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id"),
        nullable=False
    )

    salary: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 2),
        nullable=False
    )

    phone_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    department: Mapped["Department"] = relationship(
        back_populates="employees"
    )

    # Tambahkan baris ini di bagian bawah
    attendances = relationship("Attendance", back_populates="employee", cascade="all, delete-orphan")