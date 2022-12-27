import re


def parse_input(file_path):
    with open(file_path) as file:
        lines = file.read().splitlines()
        sensors_beacons = [re.findall(r'-?\d+', line) for line in lines]
        return [((int(sx), int(sy)), (int(bx), int(by))) for sx, sy, bx, by in sensors_beacons]


def get_within_range_target_y(sx, sy, bx, by, target_y):
    manhattan_distance = abs(sx - bx) + abs(sy - by)
    if abs(target_y - sy) > manhattan_distance:
        return set()
    remaining_distance = manhattan_distance - abs(target_y - sy)
    return {x for x in range(sx - remaining_distance, sx + remaining_distance + 1)}


def part_1(file_path, target_y):
    not_present_target_y = set()
    sensors_beacons = parse_input(file_path)
    for (sx, sy), (bx, by) in sensors_beacons:
        within_range_target_row = get_within_range_target_y(sx, sy, bx, by, target_y)
        not_present_target_y |= within_range_target_row
    not_present_target_y -= {sx for (sx, sy), (bx, by) in sensors_beacons if sy == target_y}
    not_present_target_y -= {bx for (sx, sy), (bx, by) in sensors_beacons if by == target_y}
    return len(not_present_target_y)


print(part_1('inputs/day_15/example_data.txt', 10))
print(part_1('inputs/day_15/data.txt', 2000000))
