from app.database.connection import SessionLocal
from app.models.department_model import Department
from app.models.employee_model import Employee


def seed_data():
    db = SessionLocal()

    try:
        # =========================
        # CREATE DEPARTMENTS
        # =========================

        implement = Department(
            name="Implement"
        )

        finance = Department(
            name="Finance"
        )

        db.add_all([
            implement,
            finance
        ])

        db.flush()

        # =========================
        # CREATE EMPLOYEES
        # =========================

        deny = Employee(
            name="Deny",
            department=implement,
            salary=10000000,
            phone_number="081234567890"
        )

        eka = Employee(
            name="Eka",
            department=finance,
            salary=8000000,
            phone_number="081234567891"
        )

        db.add_all([
            deny,
            eka
        ])

        db.commit()

        print("Seed data created successfully")

    except Exception as e:
        db.rollback()

        print(
            f"Failed to seed data: {e}"
        )

        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()