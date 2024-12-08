from pathlib import Path

file_path = Path.cwd().parent / "inputs" / f"{Path(__file__).stem}.txt"

sum_of_possible_calibration_results = 0
sum_of_possible_calibration_results_with_concat = 0


class Calibration:
    def __init__(self, expected_result, numbers, numbers_str):
        self.expected_result = expected_result
        self.numbers = numbers
        self.numbers_str = numbers_str

    def is_equation_possible(self) -> bool:
        return self._is_equation_correct(self.numbers[0], 1)

    def is_equation_possible_with_concatenation(self) -> bool:
        return self._is_equation_correct(self.numbers[0], 1, is_concat_mode=True)

    def _is_equation_correct(self, current_result, current_index, is_concat_mode=False) -> bool:
        if current_index == len(self.numbers):
            return current_result == self.expected_result
        elif current_result > self.expected_result:
            return False
        elif self._is_equation_correct(current_result + self.numbers[current_index], current_index + 1, is_concat_mode):
            return True
        elif self._is_equation_correct(current_result * self.numbers[current_index], current_index + 1, is_concat_mode):
            return True
        elif is_concat_mode:
            concat_number = int(str(current_result) + self.numbers_str[current_index])
            return self._is_equation_correct(concat_number, current_index + 1, is_concat_mode)
        else:
            return False


with file_path.open(mode="r", encoding="utf-8") as file:
    for row in file:
        calibration_result_str, parts_of_equation_str = row.split(": ")
        calibration_result = int(calibration_result_str)
        parts_of_equation = [int(x) for x in parts_of_equation_str.split()]
        calibration = Calibration(calibration_result, parts_of_equation, parts_of_equation_str.split())
        if calibration.is_equation_possible():
            sum_of_possible_calibration_results += calibration_result
            sum_of_possible_calibration_results_with_concat += calibration_result
        elif calibration.is_equation_possible_with_concatenation():
            sum_of_possible_calibration_results_with_concat += calibration_result

print(f"Total calibration result: {sum_of_possible_calibration_results}")
print(f"Total calibration result with concat: {sum_of_possible_calibration_results_with_concat}")
