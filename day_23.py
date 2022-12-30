import itertools as it
from collections import deque, Counter


def parse(filepath):
    result = set()
    with open(filepath) as file:
        lines = file.read().splitlines()
        for r, row in enumerate(lines):
            for c, symbol in enumerate(row):
                if symbol == '#':
                    result.add((r, c))
    return result


def get_prospective_position(r, c, elf_positions, directions):
    north = (r - 1, c)
    north_east = (r - 1, c + 1)
    east = (r, c + 1)
    south_east = (r + 1, c + 1)
    south = (r + 1, c)
    south_west = (r + 1, c - 1)
    west = (r, c - 1)
    north_west = (r - 1, c - 1)
    adjacent = (north, north_east, east, south_east, south, south_west, west, north_west)
    if not any(position in elf_positions for position in adjacent):  # do not need to move
        return r, c
    for direction in directions:
        if direction == 'NORTH':
            if not any(position in elf_positions for position in (north, north_east, north_west)):
                return north
        elif direction == 'SOUTH':
            if not any(position in elf_positions for position in (south, south_east, south_west)):
                return south
        elif direction == 'WEST':
            if not any(position in elf_positions for position in (west, north_west, south_west)):
                return west
        else:  # direction == 'EAST'
            if not any(position in elf_positions for position in (east, north_east, south_east)):
                return east
    return r, c  # no good options to move too


def update_elf_positions(elf_positions, directions):
    position_map = {(r, c): get_prospective_position(r, c, elf_positions, directions) for r, c in elf_positions}
    prospective_positions_count = Counter(position_map.values())
    return {current if prospective_positions_count[prospective] > 1 else prospective
            for current, prospective in position_map.items()}


def get_bounds(elf_positions):
    min_r = min(r for r, c in elf_positions)
    max_r = max(r for r, c in elf_positions)
    min_c = min(c for r, c in elf_positions)
    max_c = max(c for r, c in elf_positions)
    return min_r, max_r, min_c, max_c


def calculate_empty_ground_tiles(elf_positions):
    min_r, max_r, min_c, max_c = get_bounds(elf_positions)
    return sum(1 for r, c in it.product(range(min_r, max_r + 1), range(min_c, max_c + 1))
               if (r, c) not in elf_positions)


def display(elf_positions):
    min_r, max_r, min_c, max_c = get_bounds(elf_positions)
    return '\n'.join(''.join('#' if (r, c) in elf_positions else '.' for c in range(min_c, max_c + 1))
                     for r in range(min_r, max_r + 1)) + '\n'


def part1(filepath):
    directions = deque(('NORTH', 'SOUTH', 'WEST', 'EAST'))
    elf_positions = parse(filepath)
    for round_number in range(10):
        elf_positions = update_elf_positions(elf_positions, directions)
        directions.rotate(-1)
    return calculate_empty_ground_tiles(elf_positions)


print(part1('inputs/day_23/data.txt'))
