def parse_input(file_path):
    with open(file_path) as file:
        lines = file.read().splitlines()
        lines = [line.split(',') for line in lines]
        return {(int(x), int(y), int(z)) for x, y, z in lines}


def adjacent(x, y, z):
    return (
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1)
    )


def get_bounds(coordinates):
    min_x = min(x for x, y, z in coordinates)
    min_y = min(y for x, y, z in coordinates)
    min_z = min(z for x, y, z in coordinates)
    max_x = max(x for x, y, z in coordinates)
    max_y = max(y for x, y, z in coordinates)
    max_z = max(z for x, y, z in coordinates)
    return min_x, max_x, min_y, max_y, min_z, max_z


def is_air_bubble(start_x, start_y, start_z, coordinates, bounds):
    min_x, max_x, min_y, max_y, min_z, max_z = bounds
    seen = {(start_x, start_y, start_z)}
    to_check = [(start_x, start_y, start_z)]
    while to_check:
        next_to_check = []
        for current_x, current_y, current_z in to_check:
            if not (min_x <= current_x <= max_x and min_y <= current_y <= max_y and min_z <= current_z <= max_z):
                return False
            for adj_x, adj_y, adj_z in adjacent(current_x, current_y, current_z):
                if (adj_x, adj_y, adj_z) not in coordinates and (adj_x, adj_y, adj_z) not in seen:
                    seen.add((adj_x, adj_y, adj_z))
                    next_to_check.append((adj_x, adj_y, adj_z))
        to_check = next_to_check.copy()
    return True


def solve(file_path, part):
    coordinates = parse_input(file_path)
    bounds = get_bounds(coordinates)
    surface_area = 0
    for x, y, z in coordinates:
        for adj in adjacent(x, y, z):
            if part == 1:
                if adj not in coordinates:
                    surface_area += 1
            else:  # part == 2
                if adj not in coordinates and not is_air_bubble(*adj, coordinates, bounds):
                    surface_area += 1
    return surface_area


print(solve('inputs/day_18/data.txt', part=2))
