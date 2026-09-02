# app/routers/upload_router.py
from fastapi import APIRouter, UploadFile, File, Depends
from pydantic import BaseModel

from app.services.upload_service import UploadService
from app.dependencies.auth_dependency import get_current_user
from app.models.user_model import User

router = APIRouter(prefix="/uploads", tags=["Uploads"])

class UploadResponse(BaseModel):
    url: str

@router.post("/image", response_model=UploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user) # Karyawan biasa juga boleh upload
):
    """
    Upload foto absensi. Akan mengembalikan URL yang nantinya dikirim 
    sebagai payload 'photo_start' atau 'photo_end' saat check-in/out.
    """
    file_url = await UploadService.save_image(file)
    return {"url": file_url}