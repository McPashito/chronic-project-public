from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

from seed_new_glucose_records import create_new_glucose_records
from seed_old_glucose_records import create_old_glucose_records
from seed_users import create_demo_users


def seed_demo_data():
    print("Creando usuarios demo...")
    create_demo_users()

    print("Creando glucemias antiguas demo...")
    create_old_glucose_records()

    print("Creando glucemias nuevas demo...")
    create_new_glucose_records()

    print("Datos demo preparados correctamente.")


if __name__ == "__main__":
    seed_demo_data()
