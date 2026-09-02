# app/seed/seed_user.py
from app.database.connection import SessionLocal # Sesuaikan dengan nama session factory lu
from app.models.user_model import User
from app.core.security import get_password_hash

def seed_admin():
    db = SessionLocal()
    try:
        # Cek apakah user admin sudah ada biar gak duplikat
        existing_user = db.query(User).filter(User.username == "admin").first()
        if existing_user:
            print("🚀 User 'admin' sudah ada di database!")
            return

        # Hash password sebelum masuk database
        hashed_pw = get_password_hash("rahasia123") 
        
        # Buat object User
        admin_user = User(
            username="admin",
            hashed_password=hashed_pw,
            role="admin",
            is_active=True
        )
        
        # Simpan ke database
        db.add(admin_user)
        db.commit()
        print("✅ Berhasil membuat akun admin!")
        print("👉 Username: admin")
        print("👉 Password: rahasia123")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Terjadi error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()