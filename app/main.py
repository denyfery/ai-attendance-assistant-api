from fastapi import FastAPI

from app.routers.employee_router import router as employee_router

app = FastAPI(
    title="AI Attendance Assistant"
)

app.include_router(employee_router)

@app.get("/")
def root():
    return {
        "message":"Welcome AI Attendance Assistant"
    }