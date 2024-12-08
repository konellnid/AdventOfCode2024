from pathlib import Path

file_path = Path.cwd().parent / "inputs" / f"{Path(__file__).stem}.txt"

left_list = []
right_list = []

with file_path.open(mode="r", encoding="utf-8") as file:
    for row in file:
        elements = row.split()
        left_list.append(int(elements[0]))
        right_list.append(int(elements[1]))

left_list.sort()
right_list.sort()

sum_of_elements = 0
similarity = 0

for (left_element, right_element) in zip(left_list, right_list):
    sum_of_elements += abs(left_element - right_element)
    similarity += left_element * right_list.count(left_element)

print("Sum: ", sum_of_elements)
print("Similarity: ", similarity)
