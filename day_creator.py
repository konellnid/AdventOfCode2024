from datetime import date
from pathlib import Path
import shutil

event_start = date(2024, 12, 1)
current_date = date.today()

delta = current_date - event_start

DAYS = Path("days")
INPUTS = Path("inputs")
PYTHON_TEMPLATE_PATH = Path("days/day_template.py")


def check_python_file(day_number):
    python_file_path = DAYS / f"day_{day_number}.py"
    if not python_file_path.exists():
        shutil.copy(PYTHON_TEMPLATE_PATH, python_file_path)


def check_input_file(day_number):
    input_file_path = INPUTS / f"day_{day}.txt"
    if not input_file_path.exists():
        input_file_path.open(mode='a').close()


if __name__ == "__main__":
    delta = date.today() - event_start
    event_day_number = min(delta.days + 1, 25)

    for day in range(1, event_day_number + 1):
        check_python_file(day)
        check_input_file(day)
