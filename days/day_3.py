from pathlib import Path

import re

file_path = Path.cwd().parent / "inputs" / f"{Path(__file__).stem}.txt"

pattern_mul = r"mul\((\d{1,3})\,(\d{1,3})\)"
pattern_enable = r"do\(\)"
pattern_disable = r"don't\(\)"
pattern_whole = f"(({pattern_mul})|({pattern_enable})|({pattern_disable}))"

disable_string = "don't()"
enable_string = "do()"

sum_of_mul = 0
sum_of_mul_with_disable_switch = 0

with file_path.open(mode="r", encoding="utf-8") as file:
    is_enabled = True
    for row in file:
        for whole_word, _, mul_x, mul_y, _, _, in re.findall(pattern_whole, row):
            if whole_word == disable_string:
                is_enabled = False
            elif whole_word == enable_string:
                is_enabled = True
            else:
                sum_of_mul += int(mul_x) * int(mul_y)
                if is_enabled:
                    sum_of_mul_with_disable_switch += int(mul_x) * int(mul_y)

print(f"Sum of multiplications: {sum_of_mul}")
print(f"Sum of multiplications with disable switch: {sum_of_mul_with_disable_switch}")
