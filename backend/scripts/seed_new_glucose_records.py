from datetime import date, time, timedelta
from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

from app.db.database import SessionLocal
from app.models.glucose_records_model import GlucoseRecord
from app.models.users_model import User

START_DATE = date(2026, 4, 16)
END_DATE = date.today()

FASTING_VALUES = [64, 88, 97, 112, 132]
BEFORE_MEAL_VALUES = [68, 94, 128, 154, 188]
AFTER_MEAL_VALUES = [82, 136, 162, 178, 206]
NIGHT_VALUES = [66, 104, 142, 176, 194]


def pick_demo_value(values: list[int], user_id: int, day_counter: int, offset: int = 0):
    return values[(user_id + day_counter + offset) % len(values)]


def record_exists(db, user_id: int, record_date: date, record_time: time) -> bool:
    return (
        db.query(GlucoseRecord)
        .filter(
            GlucoseRecord.user_id == user_id,
            GlucoseRecord.date == record_date,
            GlucoseRecord.time == record_time,
        )
        .first()
        is not None
    )


def create_new_glucose_records():
    db = SessionLocal()

    try:
        users = db.query(User).order_by(User.id).all()

        if not users:
            print("No hay usuarios. Ejecuta primero el seed de usuarios.")
            return

        records_to_create = []
        current_date = START_DATE
        day_counter = 0

        while current_date <= END_DATE:
            for user in users:
                user_id = int(user.id)

                daily_records = [
                    {
                        "time": time(8, 0),
                        "glucose_value": pick_demo_value(
                            FASTING_VALUES, user_id, day_counter
                        ),
                        "moment_of_day": "fasting",
                        "notes": "Demo nuevo: ayunas con rango variado",
                    },
                    {
                        "time": time(11, 30),
                        "glucose_value": pick_demo_value(
                            BEFORE_MEAL_VALUES, user_id, day_counter, offset=1
                        ),
                        "moment_of_day": "before_meal",
                        "notes": "Demo nuevo: antes de comer con rango variado",
                    },
                    {
                        "time": time(14, 30),
                        "glucose_value": pick_demo_value(
                            AFTER_MEAL_VALUES, user_id, day_counter, offset=2
                        ),
                        "moment_of_day": "after_meal",
                        "notes": "Demo nuevo: despues de comer con rango variado",
                    },
                    {
                        "time": time(21, 30),
                        "glucose_value": pick_demo_value(
                            NIGHT_VALUES, user_id, day_counter, offset=3
                        ),
                        "moment_of_day": "night",
                        "notes": "Demo nuevo: noche con rango variado",
                    },
                ]

                for daily_record in daily_records:
                    if record_exists(db, user_id, current_date, daily_record["time"]):
                        continue

                    records_to_create.append(
                        GlucoseRecord(
                            user_id=user_id,
                            date=current_date,
                            time=daily_record["time"],
                            glucose_value=daily_record["glucose_value"],
                            notes=daily_record["notes"],
                            moment_of_day=daily_record["moment_of_day"],
                        )
                    )

            current_date += timedelta(days=1)
            day_counter += 1

        if not records_to_create:
            print(
                "No se han creado glucemias nuevas. Ya existian registros para ese rango."
            )
            return

        db.add_all(records_to_create)
        db.commit()

        print(f"Glucemias nuevas creadas correctamente: {len(records_to_create)}")

    finally:
        db.close()


if __name__ == "__main__":
    create_new_glucose_records()
