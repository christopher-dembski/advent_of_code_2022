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


def is_within_range(x, y, sx, sy, bx, by):
    manhattan_distance_sensor_beacon = abs(sx - bx) + abs(sy - by)
    manhattan_distance_point_sensor = abs(x - sx) + abs(y - sy)
    return manhattan_distance_point_sensor <= manhattan_distance_sensor_beacon


def manhattan_border(sx, sy, bx, by):
    result = set()
    manhattan_distance_plus_one = abs(sx - bx) + abs(sy - by) + 1
    for dx in range(manhattan_distance_plus_one + 1):
        dy = manhattan_distance_plus_one - dx
        result |= {(sx + dx, sy + dy), (sx + dx, sy - dy), (sx - dx, sy + dy), (sx - dx, sy - dy)}
    return result


def part_2(file_path, max_x, max_y):
    sensors_beacons = parse_input(file_path)
    just_out_of_range = set()
    for (sx, sy), (bx, by) in sensors_beacons:
        just_out_of_range |= manhattan_border(sx, sy, bx, by)
    just_out_of_range = {(x, y) for x, y in just_out_of_range if 0 <= x <= max_x and 0 <= y <= max_y}
    just_out_of_range = {(x, y) for x, y in just_out_of_range
                         if not any(is_within_range(x, y, sx, sy, bx, by) for (sx, sy), (bx, by) in sensors_beacons)}
    x, y = just_out_of_range.pop()
    return x * 4000000 + y

# print(part_1('inputs/day_15/example_data.txt', 10))
# print(part_1('inputs/day_15/data.txt', 2000000))
# print(part_2('inputs/day_15/example_data.txt', 20, 20))
# print(part_2('inputs/day_15/data.txt', 4000000, 4000000))
