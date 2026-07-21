from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.routers.employee_router import router as employee_router
from app.services.employee_service import (
    AppException,
    DuplicateEmployeeException,
    EmployeeNotFoundException,
)

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


app.include_router(employee_router)

@app.get("/")
def root():
    return {
        "message":"Welcome AI Attendance Assistant"
    }