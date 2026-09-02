# app/routers/ai_router.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services.ai_service import AIAssistantService
from app.dependencies.auth_dependency import get_current_user
from app.models.user_model import User

router = APIRouter(prefix="/ai", tags=["AI Assistant"])

class AIQueryRequest(BaseModel):
    question: str

class AIQueryResponse(BaseModel):
    answer: str

@router.post("/query", response_model=AIQueryResponse)
def ask_ai_assistant(
    payload: AIQueryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint bagi Admin/HR untuk bertanya seputar data absensi menggunakan bahasa natural.
    Contoh: "Siapa saja yang telat hari ini?" atau "Berapa orang yang sudah masuk?"
    """
    answer = AIAssistantService.ask_attendance_assistant(db, payload.question)
    return {"answer": answer}