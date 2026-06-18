from datetime import date
from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

from app.core.security import get_password_hash
from app.db.database import SessionLocal
from app.models.users_model import User

DEMO_PASSWORD = "Demo1234!"


def create_demo_users():
    db = SessionLocal()

    try:
        users_to_create = []
        existing_emails = {email for (email,) in db.query(User.email).all()}

        for i in range(1, 11):
            email = f"standard{i}@demo.com"

            if email in existing_emails:
                continue

            users_to_create.append(
                User(
                    email=email,
                    hashed_password=get_password_hash(DEMO_PASSWORD),
                    name=f"Standard{i}",
                    surname="Demo",
                    date_of_birth=date(1990, 1, i),
                    subscription_type="standard",
                )
            )

        for i in range(1, 11):
            email = f"premium{i}@demo.com"

            if email in existing_emails:
                continue

            users_to_create.append(
                User(
                    email=email,
                    hashed_password=get_password_hash(DEMO_PASSWORD),
                    name=f"Premium{i}",
                    surname="Demo",
                    date_of_birth=date(1985, 2, i),
                    subscription_type="premium",
                )
            )

        if not users_to_create:
            print("Los usuarios demo ya existen. No se crean duplicados.")
            return

        db.add_all(users_to_create)
        db.commit()

        print(f"Usuarios demo creados correctamente: {len(users_to_create)}")
        print(f"Contrasena comun: {DEMO_PASSWORD}")

    finally:
        db.close()


if __name__ == "__main__":
    create_demo_users()
