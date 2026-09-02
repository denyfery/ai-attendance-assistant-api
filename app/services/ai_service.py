# app/services/ai_service.py
import os
from groq import Groq
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from datetime import date
from app.models.attendance_model import Attendance
from app.models.employee_model import Employee
from app.core.config import settings  # 🛠️ Import settings kita

# 🛠️ Gunakan settings agar key-nya terbaca dengan aman dan presisi
client = Groq(
    api_key=settings.openai_api_key
)
MODEL_NAME = settings.ai_model_name or "gpt-4o-mini"

class AIAssistantService:
    @staticmethod
    def ask_attendance_assistant(db: Session, question: str) -> str:
        """
        AI Assistant untuk menjawab pertanyaan HR/Admin seputar absensi hari ini.
        """
        # 1. Tarik context data absensi hari ini dari database
        today = date.today()
        today_attendances = db.execute(
            select(Attendance, Employee)
            .join(Employee, Employee.id == Attendance.emp_id)
            .where(func.date(Attendance.starttime) == today)
        ).all()

        # Format data mentah jadi teks yang kaya informasi untuk AI
        context_data = []
        for att, emp in today_attendances:
            context_data.append(
                f"- Karyawan: {emp.fullname} (ID: {emp.id}), "
                f"Jam Masuk: {att.starttime}, "
                f"Jam Pulang: {att.endtime or 'Belum Check-Out'}, "
                f"Status: {att.attend_code}, "
                f"Telat: {att.actual_in} menit, "
                f"Lembur (Overtime): {att.total_ot or 0} jam / menit (Index: {att.total_otindex or 0})"
            )
        
        context_str = "\n".join(context_data) if context_data else "Belum ada data absensi untuk hari ini."

        # Perkuat System Prompt-nya
        system_prompt = f"""
        Kamu adalah AI Attendance Assistant yang cerdas untuk sistem HR perusahaan.
        Tugasmu adalah menjawab pertanyaan Administrator/HR berdasarkan data absensi hari ini di bawah ini.
        Kamu harus bisa menganalisis siapa yang lembur, berapa total jam lembur (`total_ot`), siapa yang telat, dan status kehadiran mereka.
        Jangan mengarang data di luar konteks yang diberikan. Jika data tidak ada, katakan dengan jujur.

        DATA ABSENSI HARI INI ({today}):
        {context_str}
        """

        try:
            # 3. Panggil LLM API
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                temperature=0.3,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Gagal memproses AI Assistant: {str(e)}"