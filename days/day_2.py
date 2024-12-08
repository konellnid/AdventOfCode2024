from pathlib import Path

file_path = Path.cwd().parent / "inputs" / f"{Path(__file__).stem}.txt"

# levels are safe if:
# - all decreasing or all decreasing
# - adjacent levels difference is [1, 2, 3]
number_of_safe_reports = 0
number_of_safe_reports_with_tolerance = 0


def is_safe(levels: list[int]) -> bool:
    is_increasing = all([left < right for (left, right) in zip(levels[1:], levels[:-1])])
    is_decreasing = all([left > right for (left, right) in zip(levels[1:], levels[:-1])])
    is_small_difference = all([abs(left - right) <= 3 for (left, right) in zip(levels[1:], levels[:-1])])

    return is_small_difference and (is_increasing or is_decreasing)


def is_safe_with_tolerance(levels: list[int]) -> bool:
    for i in range(len(levels)):
        levels_with_removed = levels[:i] + levels[(i + 1):]
        if is_safe(levels_with_removed):
            return True

    return False


with file_path.open(mode="r", encoding="utf-8") as file:
    for row in file:
        report_row = [int(level) for level in row.split()]

        if is_safe(report_row):
            number_of_safe_reports += 1
            number_of_safe_reports_with_tolerance += 1
        elif is_safe_with_tolerance(report_row):
            number_of_safe_reports_with_tolerance += 1

print("Safe reports: ", number_of_safe_reports)
print("Safe reports with tolerance: ", number_of_safe_reports_with_tolerance)
