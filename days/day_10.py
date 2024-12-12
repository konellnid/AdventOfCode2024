from enum import Enum
from pathlib import Path
import numpy as np

file_path = Path.cwd().parent / "inputs" / f"{Path(__file__).stem}.txt"


class Directions(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


NINE = 9


class WholeTrailHolder:
    def __init__(self):
        self.whole_trails = dict()

    def add_starting_point(self, position):
        self.whole_trails[position] = [[position]]

    def add_position(self, new_position, old_position, whole_trail):
        if new_position not in self.whole_trails:
            self.whole_trails[new_position] = []

        previous_trails = whole_trail.whole_trails[old_position]
        new_trails = []
        for trail in previous_trails:
            new_trail = trail.copy()
            new_trail.append(new_position)
            new_trails.append(new_trail)

        self.whole_trails[new_position].extend(new_trails)

    def get_trails_rating(self):
        count = 0
        for list_of_trails in self.whole_trails.values():
            count += len(list_of_trails)
        return count


class TrailHolder:
    def __init__(self):
        self.starting_points_holder = dict()
        self.whole_trails_holder = dict()

    def add_position(self, position, sources):
        if position in self.starting_points_holder.keys():
            self.starting_points_holder[position].update(sources)
        else:
            self.starting_points_holder[position] = set(sources)

    def get_positions(self):
        return self.starting_points_holder.keys()

    def get_starting_points_for_position(self, position):
        return self.starting_points_holder[position]

    def count_trails_score(self) -> int:
        count = 0
        for starting_points in self.starting_points_holder.values():
            count += len(starting_points)
        return count


def create_tuple_from_position(height_nine_position):
    return height_nine_position[0], height_nine_position[1]


class HikingTrail:
    def __init__(self, grid):
        self.whole_trail = WholeTrailHolder()
        self.trail = TrailHolder()
        self.grid: np.ndarray[int, int] = np.pad(grid, (1, 1), "constant", constant_values=(-99, -99))
        self.directional_grids = {}
        self.create_directional_grids()
        self.sum_of_scores = 0

        self.find_valid_trails()

    def find_valid_trails(self):
        trail = TrailHolder()
        whole_trail = WholeTrailHolder()
        for height_nine_position in np.argwhere(self.grid == NINE):
            position = create_tuple_from_position(height_nine_position)
            trail.add_position(position, [position])
            whole_trail.add_starting_point(position)

        current_height = NINE

        while current_height > 0:
            lower_height_trail = TrailHolder()
            lower_height_whole_trail = WholeTrailHolder()

            for position in trail.get_positions():
                for direction in Directions:
                    direction_grid = self.directional_grids[direction]
                    if direction_grid[position]:
                        new_position = (position[0] + direction.value[0], position[1] + direction.value[1])
                        lower_height_trail.add_position(new_position, trail.get_starting_points_for_position(position))
                        lower_height_whole_trail.add_position(new_position, position, whole_trail)

            trail = lower_height_trail
            whole_trail = lower_height_whole_trail
            current_height -= 1

        self.trail = trail
        self.whole_trail = whole_trail

    def create_directional_grids(self):
        self.directional_grids[Directions.UP] = (self.grid - np.roll(self.grid, 1, 0)) == 1
        self.directional_grids[Directions.DOWN] = (self.grid - np.roll(self.grid, -1, 0)) == 1
        self.directional_grids[Directions.LEFT] = (self.grid - np.roll(self.grid, 1, 1)) == 1
        self.directional_grids[Directions.RIGHT] = (self.grid - np.roll(self.grid, -1, 1)) == 1

    def get_trails_score(self):
        return self.trail.count_trails_score()

    def get_trails_rating(self):
        return self.whole_trail.get_trails_rating()


with file_path.open(mode="r", encoding="utf-8") as file:
    rows = list()
    for row in file.readlines():
        row_int = [int(x) for x in list(row.strip())]
        rows.append(row_int)

    array_grid = np.array(rows, dtype=object)
    hiking_trail = HikingTrail(array_grid)

    print(f"Trails score: {hiking_trail.get_trails_score()}")
    print(f"Trails rating: {hiking_trail.get_trails_rating()}")
