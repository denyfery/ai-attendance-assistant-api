from app.database.base import Base
from app.database.connection import engine
from app.models.employee_model import Employee

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Tables created successfully")