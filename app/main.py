from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.services.employee_service import (
    AppException,
    DuplicateEmployeeException,
    EmployeeNotFoundException,
)

from app.routers import auth_router, employee_router, attendance_router, upload_router, ai_router
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title="AI Attendance Assistant"
)

@app.exception_handler(AppException)
async def app_exception_handler(request, exc: AppException):
    if isinstance(exc, EmployeeNotFoundException):
        status_code = 404
    elif isinstance(exc, DuplicateEmployeeException):
        status_code = 409
    else:
        status_code = 400

    return JSONResponse(
        status_code=status_code,
        content={"detail": exc.message},
    )

@app.get("/")
def root():
    return {
        "message":"Welcome AI Attendance Assistant"
    }

# Buat folder uploads otomatis kalau belum ada pas server jalan
os.makedirs("uploads", exist_ok=True)
# Mount folder uploads biar bisa diakses via HTTP
app.mount("/static", StaticFiles(directory="uploads"), name="static")

# Daftarkan router
app.include_router(employee_router.router)
app.include_router(auth_router.router)
app.include_router(attendance_router.router)
app.include_router(upload_router.router)
app.include_router(ai_router.router)