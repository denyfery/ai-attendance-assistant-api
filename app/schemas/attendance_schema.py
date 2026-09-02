# app/schemas/attendance_schema.py
import re
import ipaddress
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Generic, TypeVar, Literal

T = TypeVar("T")

class AttendanceCreate(BaseModel):
    attend_id: str
    emp_id: int
    # Membatasi pilihan tipe hari: Workday, Weekend, Holiday
    daytype: Literal["WD", "WE", "HOL"] = "WD" 
    # Membatasi status kehadiran
    attend_code: Literal["present", "late", "absent", "leave"] | None = None
    
    starttime: datetime | None = None
    
    geoloc_start: str | None = None
    photo_start: str | None = None
    ip_starttime: str | None = None

    # 1. Validasi Format Titik Koordinat GPS
    @field_validator("geoloc_start", mode="before")
    @classmethod
    def validate_geoloc(cls, value: str | None):
        if value:
            # Regex untuk format "Latitude, Longitude"
            pattern = r"^-?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*-?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$"
            if not re.match(pattern, value):
                raise ValueError("Format koordinat salah. Gunakan format 'Latitude, Longitude'")
        return value

    # 2. Validasi Ekstensi File Foto
    @field_validator("photo_start", mode="before")
    @classmethod
    def validate_photo_ext(cls, value: str | None):
        if value:
            if not value.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                raise ValueError("Format foto tidak valid. Gunakan .jpg, .jpeg, .png, atau .webp")
        return value

    # 3. Validasi IP Address
    @field_validator("ip_starttime", mode="before")
    @classmethod
    def validate_ip(cls, value: str | None):
        if value:
            try:
                ipaddress.ip_address(value)
            except ValueError:
                raise ValueError("Format IP Address tidak valid")
        return value


class AttendanceUpdate(BaseModel):
    endtime: datetime | None = None
    attend_code: Literal["present", "late", "absent", "leave"] | None = None
    actual_in: int | None = None
    actual_out: int | None = None
    actualworkmnt: int | None = None
    total_ot: float | None = None
    total_otindex: float | None = None
    remark: str | None = None
    
    geoloc_end: str | None = None
    photo_end: str | None = None
    ip_endtime: str | None = None

    # Validasi yang sama diterapkan untuk waktu kepulangan (end)
    @field_validator("geoloc_end", mode="before")
    @classmethod
    def validate_geoloc(cls, value: str | None):
        if value:
            pattern = r"^-?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*-?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$"
            if not re.match(pattern, value):
                raise ValueError("Format koordinat salah. Gunakan format 'Latitude, Longitude'")
        return value

    @field_validator("photo_end", mode="before")
    @classmethod
    def validate_photo_ext(cls, value: str | None):
        if value:
            if not value.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                raise ValueError("Format foto tidak valid. Gunakan .jpg, .jpeg, .png, atau .webp")
        return value

    @field_validator("ip_endtime", mode="before")
    @classmethod
    def validate_ip(cls, value: str | None):
        if value:
            try:
                ipaddress.ip_address(value)
            except ValueError:
                raise ValueError("Format IP Address tidak valid")
        return value


class AttendanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    attend_id: str
    emp_id: int
    daytype: str
    attend_code: str | None = None
    shiftstarttime: datetime | None = None
    shiftendtime: datetime | None = None
    starttime: datetime | None = None
    endtime: datetime | None = None
    actualworkmnt: int | None = None
    created_date: datetime
    created_by: str
    modified_date: datetime
    modified_by: str

class PaginationResponse(BaseModel, Generic[T]):
    data: list[T]
    has_more: bool
    next_cursor: str | None = None

class AttendancePaginationResponse(PaginationResponse[AttendanceResponse]):
    pass