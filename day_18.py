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


def part_1(file_path):
    coordinates = parse_input(file_path)
    surface_area = 0
    for x, y, z in coordinates:
        for adj in adjacent(x, y, z):
            if adj not in coordinates:
                surface_area += 1
    return surface_area


print(part_1('inputs/day_18/data.txt'))
