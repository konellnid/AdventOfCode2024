from enum import Enum
from pathlib import Path
import numpy as np

file_path = Path.cwd().parent / "inputs" / f"{Path(__file__).stem}.txt"

XMAS_STRING = "XMAS"
LETTER_X = "X"
LETTER_M = "M"
LETTER_A = "A"
LETTER_S = "S"


class Direction(Enum):
    UP = (0, 1)
    UP_RIGHT = (1, 1)
    RIGHT = (1, 0)
    BOTTOM_RIGHT = (1, -1)
    BOTTOM = (0, -1)
    BOTTOM_LEFT = (-1, -1)
    LEFT = (-1, 0)
    UP_LEFT = (-1, 1)


class LetterIndex(Enum):
    X = 0
    M = 1
    A = 2
    S = 3


class WholeGrid:
    def __init__(self, grid):
        self.grid = grid
        self.width, self.height = grid.shape
        self.xmas_counter = 0

    def find_xmas(self):
        self.xmas_counter = 0
        self.xmas_x_counter = 0

        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y] == XMAS_STRING[LetterIndex.X.value]:
                    self.search_from_place(x, y)

    def search_from_place(self, x, y):
        for direction in Direction:
            self.search_from_place_in_direction(x + direction.value[0],
                                                y + direction.value[1],
                                                direction,
                                                LetterIndex.M.value)

    def search_from_place_in_direction(self, x, y, direction, current_letter_number):
        if current_letter_number == 4:
            self.xmas_counter += 1  # XMAS found!
        elif self.is_within_bounds(x, y) and self.grid[x][y] == XMAS_STRING[current_letter_number]:
            self.search_from_place_in_direction(x + direction.value[0],
                                                y + direction.value[1],
                                                direction,
                                                current_letter_number + 1)

    def is_within_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def find_x_xmas(self):
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                if self.grid[x][y] == "A":
                    self.check_diagonals_for_xmas(x, y)

    def check_diagonals_for_xmas(self, x, y):
        top_left = self.grid[x - 1][y + 1]
        top_right = self.grid[x + 1][y + 1]
        bottom_right = self.grid[x + 1][y - 1]
        bottom_left = self.grid[x - 1][y - 1]

        if self.is_x_xmas_diagonal(top_left, bottom_right) and self.is_x_xmas_diagonal(top_right, bottom_left):
            self.xmas_x_counter += 1

    def is_x_xmas_diagonal(self, letter_1, letter_2):
        return (letter_1, letter_2) == (LETTER_M, LETTER_S) or (letter_1, letter_2) == (LETTER_S, LETTER_M)


with file_path.open(mode="r", encoding="utf-8") as file:
    rows = list()
    for row in file.readlines():
        rows.append(list(row.strip()))

    array_grid = np.array(rows, dtype=object)
    whole_grid = WholeGrid(array_grid)
    whole_grid.find_xmas()
    whole_grid.find_x_xmas()

print(f"Found XMAS counter: {whole_grid.xmas_counter}")
print(f"Found X-MAS counter: {whole_grid.xmas_x_counter}")
