import string

PRIORITY_DICT = {letter: i + 1 for i, letter in enumerate(string.ascii_lowercase + string.ascii_uppercase)}


def parse_input_part_1(data_file_path):
    with open(data_file_path) as file:
        lines = file.read().splitlines()
        return [(line[:len(line) // 2], line[len(line) // 2:]) for line in lines]


def part_1(data_file_path):
    rucksacks = parse_input_part_1(data_file_path)
    priority_sum = 0
    for compartment_1, compartment_2 in rucksacks:
        common_letter = (set(compartment_1) & set(compartment_2)).pop()
        priority_sum += PRIORITY_DICT[common_letter]
    return priority_sum


# output: [('sack1_group1', 'sack2_group1', 'sack3_group1'), ...]
def parse_input_part_2(data_file_path):
    with open(data_file_path) as file:
        lines = file.read().splitlines()
        number_of_lines = len(lines)
        lines = iter(lines)
        return [(next(lines), next(lines), next(lines)) for group_number in range(number_of_lines // 3)]


def part_2(data_file_path):
    groups = parse_input_part_2(data_file_path)
    priority_sum = 0
    for sack1, sack2, sack3 in groups:
        common_letter = (set(sack1) & set(sack2) & set(sack3)).pop()
        priority_sum += PRIORITY_DICT[common_letter]
    return priority_sum


print(part_1('inputs/day_3/data.txt'))
print(part_2('inputs/day_3/data.txt'))
