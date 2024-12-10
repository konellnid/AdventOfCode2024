from pathlib import Path
import numpy as np

file_path = Path.cwd().parent / "inputs" / f"{Path(__file__).stem}.txt"

EMPTY_FIELD_SYMBOL = "."
ANTI_NODE_SYMBOL = "#"


class AntennaField:
    def __init__(self, grid):
        self.grid: np.ndarray = grid
        self.simple_anti_nodes_grid = np.empty_like(grid)  # part 1 grid
        self.harmonics_anti_nodes_grid = np.empty_like(grid)  # part 2 grid

        self.antenna_symbols = set(np.unique(grid))
        self.antenna_symbols.remove(EMPTY_FIELD_SYMBOL)

        self.find_anti_nodes_positions()

    def is_within_bounds(self, x, y):
        return 0 <= x < self.grid.shape[0] and 0 <= y < self.grid.shape[1]

    def find_anti_nodes_positions(self):
        for antenna_symbol in self.antenna_symbols:
            same_symbol_antenna_positions = np.argwhere(self.grid == antenna_symbol)
            self.mark_overlapping_frequencies(same_symbol_antenna_positions)

    def mark_overlapping_frequencies(self, antenna_positions: np.ndarray):
        for (first_antenna_x, first_antenna_y) in antenna_positions:
            for (second_antenna_x, second_antenna_y) in antenna_positions:
                if first_antenna_x != second_antenna_x or first_antenna_y != second_antenna_y:
                    self.mark_simple_anti_nodes(first_antenna_x, first_antenna_y, second_antenna_x, second_antenna_y)
                    self.mark_harmonics_anti_nodes(first_antenna_x, first_antenna_y, second_antenna_x, second_antenna_y)

    def mark_simple_anti_nodes(self, x_1, y_1, x_2, y_2):
        (diff_x, diff_y) = (x_2 - x_1, y_2 - y_1)

        new_x, new_y = x_1 - diff_x, y_1 - diff_y
        if self.is_within_bounds(new_x, new_y):
            self.mark_anti_node(new_x, new_y)

        new_x, new_y = x_2 + diff_x, y_2 + diff_y
        if self.is_within_bounds(new_x, new_y):
            self.mark_anti_node(new_x, new_y)

    def mark_harmonics_anti_nodes(self, x_1, y_1, x_2, y_2):
        (diff_x, diff_y) = (x_2 - x_1, y_2 - y_1)

        self.mark_harmonics_in_direction(x_1, y_1, diff_x, diff_y)
        self.mark_harmonics_in_direction(x_2, y_2, -diff_x, -diff_y)

    def mark_anti_node(self, x, y):
        self.simple_anti_nodes_grid[x][y] = ANTI_NODE_SYMBOL

    def mark_harmonics_in_direction(self, x, y, diff_x, diff_y):
        new_x, new_y = x + diff_x, y + diff_y
        while self.is_within_bounds(new_x, new_y):
            self.harmonics_anti_nodes_grid[new_x, new_y] = ANTI_NODE_SYMBOL
            new_x, new_y = new_x + diff_x, new_y + diff_y
            print(new_x, new_y)

    def count_simple_anti_nodes(self):
        return np.count_nonzero(self.simple_anti_nodes_grid == ANTI_NODE_SYMBOL)

    def count_harmonics_anti_nodes(self):
        return np.count_nonzero(self.harmonics_anti_nodes_grid == ANTI_NODE_SYMBOL)


with file_path.open(mode="r", encoding="utf-8") as file:
    rows = list()
    for row in file.readlines():
        rows.append(list(row.strip()))

    array_grid = np.array(rows, dtype=object)
    print(array_grid)
    antenna_field = AntennaField(array_grid)

    print(f"Number of simple antinodes: {antenna_field.count_simple_anti_nodes()}")
    print(f"Number of harmonics antinodes: {antenna_field.count_harmonics_anti_nodes()}")
