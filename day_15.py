import re


def parse_input(file_path):
    with open(file_path) as file:
        lines = file.read().splitlines()
        sensors_beacons = [re.findall(r'-?\d+', line) for line in lines]
        return [((int(sx), int(sy)), (int(bx), int(by))) for sx, sy, bx, by in sensors_beacons]


def get_within_range(sx, sy, bx, by):
    manhattan_distance = abs(sx - bx) + abs(sy - by)
    result = {(sx, sy)}
    for step in range(manhattan_distance):
        for x, y in result.copy():
            result |= {(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)}
    return result


def part_1(file_path, target_y):
    not_present = set()
    sensors_beacons = parse_input(file_path)
    sensors_set = {(sx, sy) for (sx, sy), (bx, by) in sensors_beacons}
    beacons_set = {(bx, by) for (sx, sy), (bx, by) in sensors_beacons}
    for (sx, sy), (bx, by) in sensors_beacons:
        within_range = get_within_range(sx, sy, bx, by)
        not_present |= within_range
    not_present -= sensors_set
    not_present -= beacons_set
    return sum(1 for x, y in not_present if y == target_y)


# print(part_1('inputs/day_15/example_data.txt', 10))
# print(part_1('inputs/day_15/data.txt', 2000000))
