import copy
from enum import Enum
from pathlib import Path
import numpy as np
from sympy.strategies.core import switch

file_path = Path.cwd().parent / "inputs" / f"{Path(__file__).stem}.txt"

EMPTY_SPACE_SYMBOL = "."
OBSTACLE_SYMBOL = "#"
WALKED_PATH_SYMBOL = "X"
GUARD_SYMBOL = "^"
SIMULATION_PLACEHOLDER = "?"


class Direction(Enum):
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)
    UP = (-1, 0)

    def rotate_clockwise(self):
        direction_order = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        current_index = direction_order.index(self)
        return direction_order[(current_index + 1) % len(direction_order)]


class GuardMap:
    def __init__(self, grid: np.ndarray):
        self.grid: np.ndarray = grid
        self.current_guard_position = tuple(np.argwhere(self.grid == GUARD_SYMBOL)[0])
        self.obstacle_placement_count = 0
        self.directional_maps = dict()
        for direction in Direction:
            self.directional_maps[direction] = grid.copy()

    def mark_walking_path(self):
        self.go_in_direction()

    def go_in_direction(self):
        self.grid[self.current_guard_position] = WALKED_PATH_SYMBOL
        current_direction = Direction.UP
        next_position = tuple(np.array(self.current_guard_position) + np.array(current_direction.value))

        while self.is_within_bounds(next_position):
            self.directional_maps[current_direction][self.current_guard_position] = WALKED_PATH_SYMBOL

            if self.grid[next_position] == OBSTACLE_SYMBOL:
                current_direction = current_direction.rotate_clockwise()
            else:
                self.check_for_obstacle_placement(next_position, current_direction)
                self.current_guard_position = next_position

            self.grid[self.current_guard_position] = WALKED_PATH_SYMBOL
            next_position = self.find_next_position(current_direction)

    def is_within_bounds(self, position):
        return 0 <= position[0] < self.grid.shape[0] \
            and 0 <= position[1] < self.grid.shape[1]

    def count_walked_spaces(self):
        return np.count_nonzero(self.grid == WALKED_PATH_SYMBOL)

    def check_for_obstacle_placement(self, next_position, current_direction):
        if self.grid[next_position] == EMPTY_SPACE_SYMBOL:
            self.grid[next_position] = OBSTACLE_SYMBOL
            if self.is_loop(next_position, current_direction):
                self.obstacle_placement_count += 1
                print(self.obstacle_placement_count)
            self.clean_tmp_placements()
            # reverse obstacle placement
            self.grid[next_position] = EMPTY_SPACE_SYMBOL

    def find_next_position(self, direction):
        return tuple(np.array(self.current_guard_position) + np.array(direction.value))

    def is_loop(self, next_position, current_direction) -> bool:
        while self.is_within_bounds(next_position):
            if self.directional_maps[current_direction][next_position] in (WALKED_PATH_SYMBOL, SIMULATION_PLACEHOLDER):
                return True

            if self.grid[next_position] == OBSTACLE_SYMBOL:
                current_direction = current_direction.rotate_clockwise()
            else:
                self.current_guard_position = next_position
                if self.grid[self.current_guard_position] == EMPTY_SPACE_SYMBOL:
                    self.grid[self.current_guard_position] = SIMULATION_PLACEHOLDER
                if self.directional_maps[current_direction][self.current_guard_position] == EMPTY_SPACE_SYMBOL:
                    self.directional_maps[current_direction][self.current_guard_position] = SIMULATION_PLACEHOLDER

            next_position = self.find_next_position(current_direction)

        # Guard went out of bounds
        return False

    def clean_tmp_placements(self):
        self.grid[self.grid == SIMULATION_PLACEHOLDER] = EMPTY_SPACE_SYMBOL
        for directional_grid in self.directional_maps.values():
            directional_grid[directional_grid == SIMULATION_PLACEHOLDER] = EMPTY_SPACE_SYMBOL


with file_path.open(mode="r", encoding="utf-8") as file:
    rows = list()
    for row in file.readlines():
        rows.append(list(row.strip()))

    array_grid = np.array(rows, dtype=object)
    guard_map = GuardMap(array_grid)
    guard_map.mark_walking_path()
    print(f"Walked spaces {guard_map.count_walked_spaces()}")
    print(f"Possible obstacle placements: {guard_map.obstacle_placement_count}")

    # print the path walked
    # with open('Solution.txt', mode='w') as solution_write:
    #     for row in guard_map.grid:
    #         for element in row:
    #             solution_write.write(element)
    #         solution_write.write('\n')
