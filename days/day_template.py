from pathlib import Path

file_path = Path.cwd().parent / "inputs" / f"{Path(__file__).stem}.txt"

with file_path.open(mode="r", encoding="utf-8") as file:
    for row in file:
        print(row)
