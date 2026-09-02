# app/services/upload_service.py
import os
import uuid
import urllib.request
import cv2
import numpy as np
from pathlib import Path
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = Path("uploads")

# 🛠️ AUTO-DOWNLOAD MODEL FACE DETECTION JIKA BELUM ADA DI PROJECT
CASCADE_FILE = "haarcascade_frontalface_default.xml"
if not os.path.exists(CASCADE_FILE):
    print("Mendownload model Haar Cascade OpenCV...")
    url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
    urllib.request.urlretrieve(url, CASCADE_FILE)

# Load model dari file lokal yang sudah di-download
face_cascade = cv2.CascadeClassifier(CASCADE_FILE)

# Validasi memastikan model benar-benar ter-load
if face_cascade.empty():
    raise RuntimeError("Gagal memuat model Face Detection. Cek file XML.")

class UploadService:
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

    @staticmethod
    async def detect_face(image_bytes: bytes) -> bool:
        """
        Fungsi AI menggunakan OpenCV Haar Cascade untuk mendeteksi wajah dalam gambar.
        """
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="File gambar rusak atau tidak bisa dibaca.")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(30, 30)
        )
        
        if len(faces) == 0:
            raise HTTPException(status_code=400, detail="Wajah tidak terdeteksi! Pastikan foto wajah Anda menghadap kamera dengan jelas.")
        
        if len(faces) > 1:
            raise HTTPException(status_code=400, detail="Terdeteksi lebih dari satu wajah. Pastikan hanya ada Anda di dalam foto.")
                
        return True

    @staticmethod
    async def save_image(file: UploadFile) -> str:
        ext = Path(file.filename).suffix.lower()
        if ext not in UploadService.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"Ekstensi {ext} tidak diizinkan. Gunakan .jpg, .jpeg, .png, atau .webp"
            )

        image_bytes = await file.read()
        
        if len(image_bytes) > UploadService.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="Ukuran file maksimal 5MB")

        # 3. 🤖 AI FACE DETECTION
        await UploadService.detect_face(image_bytes)

        unique_filename = f"{uuid.uuid4().hex}{ext}"
        file_path = UPLOAD_DIR / unique_filename

        try:
            with file_path.open("wb") as buffer:
                buffer.write(image_bytes)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Gagal menyimpan file gambar")
        finally:
            await file.close()

        return f"/static/{unique_filename}"