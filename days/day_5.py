from enum import Enum
from pathlib import Path
import numpy as np

file_path = Path.cwd().parent / "inputs" / f"{Path(__file__).stem}.txt"

RESTRICTION_SEPARATOR = '|'
PAGES_SEPARATOR = ','


class RestrictionFrom:
    def __init__(self, pre, post):
        self.pre = pre
        self.post = post


class Validator:
    def __init__(self):
        self.restriction_pre_holder: dict[int, set] = dict()
        self.restriction_post_holder: dict[int, set] = dict()

    def add_restriction(self, page_pre, page_post):
        self._update_restrictions_dict(page_pre, page_post, self.restriction_pre_holder)
        self._update_restrictions_dict(page_post, page_pre, self.restriction_post_holder)

    def _update_restrictions_dict(self, x, y, restriction_dict: dict[int, set]):
        if x in restriction_dict.keys():
            restriction_dict[x].add(y)
        else:
            restriction_dict[x] = {y}

    def is_valid(self, page_numbers: list[int]) -> bool:
        disallowed_page_numbers = set()
        for page in page_numbers:
            if page in disallowed_page_numbers:
                return False
            else:
                disallowed_page_numbers.update(self.restriction_post_holder[page])
        return True

    def reorder(self, page_numbers: list[int]) -> list[int]:
        new_order = [page_numbers[0]]
        for page in page_numbers[1:]:
            new_order = self.make_valid_insert(new_order, page)
        return new_order

    def make_valid_insert(self, new_order, page):
        new_order_tryout = new_order.copy() + [page]
        for insert_index in reversed(range(len(new_order) + 1)):
            new_order_tryout = new_order.copy()
            new_order_tryout.insert(insert_index, page)
            if self.is_valid(new_order_tryout):
                return new_order_tryout

        return new_order_tryout


sum_of_valid_middle_page_numbers = 0
sum_of_reordered_middle_page_numbers = 0

with file_path.open(mode="r", encoding="utf-8") as file:
    validator = Validator()

    rows = list()
    for row in file.readlines():
        if RESTRICTION_SEPARATOR in row:
            (restriction_pre, restriction_post) = row.split('|')
            validator.add_restriction(int(restriction_pre), int(restriction_post))
        elif PAGES_SEPARATOR in row:
            pages = [int(page) for page in row.split(PAGES_SEPARATOR)]
            if validator.is_valid(pages):
                sum_of_valid_middle_page_numbers += pages[len(pages) // 2]
            else:
                reordered_pages = validator.reorder(pages)
                sum_of_reordered_middle_page_numbers += reordered_pages[len(pages) // 2]

print(f"Sum of valid middle page numbers: {sum_of_valid_middle_page_numbers}")
print(f"Sum of reordered middle page numbers: {sum_of_reordered_middle_page_numbers}")
