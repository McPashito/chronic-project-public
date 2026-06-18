from datetime import date, time, timedelta, datetime, timezone
from pathlib import Path
import sys

from sqlalchemy import text

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

from app.db.database import SessionLocal
from app.models.users_model import User

START_DATE = date(2026, 2, 14)
END_DATE = date(2026, 4, 15)


def create_old_glucose_records():
    db = SessionLocal()

    try:
        existing_records = db.execute(
            text("SELECT COUNT(*) FROM glucose_records")
        ).scalar()

        if existing_records > 0:
            print("Ya existen glucemias en la base de datos. No se crean duplicados.")
            return

        users = db.query(User).order_by(User.id).all()

        if not users:
            print("No hay usuarios. Ejecuta primero el seed de usuarios.")
            return

        records_to_create = []
        current_date = START_DATE
        day_counter = 0

        while current_date <= END_DATE:
            for user in users:
                base_value = 85 + (user.id % 10) * 4

                records_to_create.append(
                    {
                        "user_id": user.id,
                        "date": current_date,
                        "time": time(8, 0),
                        "glucose_value": base_value + (day_counter % 15),
                        "notes": "Demo antiguo: ayunas sin moment_of_day",
                        "created_at": datetime.now(timezone.utc),
                        "updated_at": datetime.now(timezone.utc),
                    }
                )

                records_to_create.append(
                    {
                        "user_id": user.id,
                        "date": current_date,
                        "time": time(14, 30),
                        "glucose_value": base_value + 35 + (day_counter % 25),
                        "notes": "Demo antiguo: tarde sin moment_of_day",
                        "created_at": datetime.now(timezone.utc),
                        "updated_at": datetime.now(timezone.utc),
                    }
                )

                records_to_create.append(
                    {
                        "user_id": user.id,
                        "date": current_date,
                        "time": time(21, 30),
                        "glucose_value": base_value + 20 + (day_counter % 30),
                        "notes": "Demo antiguo: noche sin moment_of_day",
                        "created_at": datetime.now(timezone.utc),
                        "updated_at": datetime.now(timezone.utc),
                    }
                )

            current_date += timedelta(days=1)
            day_counter += 1

        db.execute(
            text("""
                INSERT INTO glucose_records
                    (user_id, date, time, glucose_value, notes, created_at, updated_at)
                VALUES
                    (:user_id, :date, :time, :glucose_value, :notes, :created_at, :updated_at)
            """),
            records_to_create,
        )

        db.commit()

        print(f"Glucemias antiguas creadas correctamente: {len(records_to_create)}")

    finally:
        db.close()


if __name__ == "__main__":
    create_old_glucose_records()
