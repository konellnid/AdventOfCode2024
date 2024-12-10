from pathlib import Path

file_path = Path.cwd().parent / "inputs" / f"{Path(__file__).stem}.txt"


class DiskMapFragmented:
    def __init__(self, data: list[int]):
        self.files: list[int] = data[0::2]
        self.empty_spaces: list[int] = data[1::2]

        self.is_initial_file_place = True
        self.current_index_left = 0
        self.current_index_right = len(self.files) - 1
        self.empty_spaces_index = 0
        self.right_side_leftover = self.files[self.current_index_right]
        self.empty_space_leftover = self.empty_spaces[0]

        self.checksum = 0
        self.calculate_checksum()

    def calculate_checksum(self):
        current_position = 0
        while self.current_index_left != self.current_index_right:
            if self.is_initial_file_place:
                for _ in range(self.files[self.current_index_left]):
                    self.checksum += current_position * self.current_index_left
                    current_position += 1
                self.current_index_left += 1
                self.is_initial_file_place = False
            elif self.empty_space_leftover == 0:
                self.empty_spaces_index += 1
                self.empty_space_leftover = self.empty_spaces[self.empty_spaces_index]
                self.is_initial_file_place = True
            else:
                if self.right_side_leftover == 0:
                    self.current_index_right -= 1
                    self.right_side_leftover = self.files[self.current_index_right]
                else:
                    to_put = min(self.empty_space_leftover, self.right_side_leftover)
                    for x in range(to_put):
                        self.checksum += current_position * self.current_index_right
                        self.empty_space_leftover -= 1
                        self.right_side_leftover -= 1
                        current_position += 1
        # post loop
        for _ in range(self.right_side_leftover):
            self.checksum += current_position * self.current_index_right
            current_position += 1


class EmptySpaceReplacement:
    def __init__(self):
        self.held_files: list[int] = list()
        self.held_files_sizes: list[int] = list()

    def add_file(self, file_id: int, file_size: int):
        self.held_files.append(file_id)
        self.held_files_sizes.append(file_size)

    def get_empty_space_replacement(self):
        return zip(self.held_files, self.held_files_sizes)


class DiskMapWholeFiles:
    def __init__(self, data: list[int]):
        self.files: list[int] = data[0::2]
        self.empty_spaces: list[int] = data[1::2]

        self.is_initial_file_place = True
        self.current_index_left = 0
        self.current_index_right = len(self.files) - 1
        self.empty_spaces_index = 0
        self.empty_space_leftover = self.empty_spaces[0]

        self.checksum = 0
        self.empty_space_index_file_placement: dict[int, EmptySpaceReplacement] = dict()
        self.moved_files = set()

        self.calculate_checksum()

    def calculate_checksum(self):
        current_position = 0
        for empty_space_index in range(len(self.empty_spaces)):
            self.empty_space_index_file_placement[empty_space_index] = EmptySpaceReplacement()

        for index_right in reversed(range(len(self.files))):
            self.try_moving_file(index_right)

        for index_left in range(len(self.files) - 1):
            for _ in range(self.files[index_left]):
                if not index_left in self.moved_files:
                    self.checksum += current_position * index_left
                current_position += 1

            if index_left < len(self.empty_spaces):
                empty_space_replacement = self.empty_space_index_file_placement[index_left]
                for file_id, file_size in empty_space_replacement.get_empty_space_replacement():
                    for _ in range(file_size):
                        self.checksum += current_position * file_id
                        current_position += 1

                if self.empty_spaces[index_left] > 0:
                    current_position += self.empty_spaces[index_left]

    def try_moving_file(self, file_id):
        file_size = self.files[file_id]
        for empty_space_index in range(file_id):
            if file_size <= self.empty_spaces[empty_space_index]:
                self.empty_space_index_file_placement[empty_space_index].add_file(file_id, file_size)
                self.empty_spaces[empty_space_index] = self.empty_spaces[empty_space_index] - file_size
                self.moved_files.add(file_id)
                return  # successful file movement


with file_path.open(mode="r", encoding="utf-8") as file:
    data = [int(x) for x in file.readline()]
    disk_map_fragmented_files = DiskMapFragmented(data)
    print(f"Checksum for fragmented files: {disk_map_fragmented_files.checksum}")
    disk_map_whole_files = DiskMapWholeFiles(data)
    print(f"Checksum for whole files: {disk_map_whole_files.checksum}")
