NORTH = (-1, 0)
EAST = (0, 1)
SOUTH = (1, 0)
WEST = (0, -1)


def parse_input(filepath):
    blizzards = set()
    walls = set()
    with open(filepath) as file:
        lines = file.read().splitlines()
        for r, row in enumerate(lines):
            for c, symbol in enumerate(row):
                if symbol == '#':
                    walls.add((r, c))
                if symbol == '^':
                    blizzards.add(((r, c), NORTH))
                elif symbol == '>':
                    blizzards.add(((r, c), EAST))
                elif symbol == 'v':
                    blizzards.add(((r, c), SOUTH))
                elif symbol == '<':
                    blizzards.add(((r, c), WEST))
    return blizzards, walls


def get_grid(blizzards, walls, max_row, max_col):
    def get_symbol(rc):
        num_blizzards = sum((rc, direction) in blizzards for direction in (NORTH, EAST, SOUTH, WEST))
        if rc in walls:
            return '#'
        elif num_blizzards > 1:
            return str(num_blizzards)
        elif (rc, NORTH) in blizzards:
            return '^'
        elif (rc, EAST) in blizzards:
            return '>'
        elif (rc, SOUTH) in blizzards:
            return 'v'
        elif (rc, WEST) in blizzards:
            return '<'
        else:
            return '.'

    return '\n'.join(''.join(get_symbol((r, c)) for c in range(max_col + 1)) for r in range(max_row + 1)) + '\n'


def update_blizzards(blizzards, max_r, max_c):
    new_blizzards = set()
    for (r, c), (dr, dc) in blizzards:
        new_row = r + dr
        new_col = c + dc
        if new_row == 0:
            new_row = max_r - 1
        elif new_row == max_r:
            new_row = 1
        elif new_col == 0:
            new_col = max_c - 1
        elif new_col == max_c:
            new_col = 1
        new_blizzards.add(((new_row, new_col), (dr, dc)))
    return new_blizzards


def update_positions(positions, blizzards, walls):
    def blizzard_collision(p):
        return any((p, dv) in blizzards for dv in (NORTH, EAST, SOUTH, WEST))

    new_positions = set()
    for r, c in positions:
        same = (r, c)
        north = (r - 1, c)
        east = (r, c + 1)
        south = (r + 1, c)
        west = (r, c - 1)
        new_positions |= {p for p in (same, north, east, south, west) if p not in walls and not blizzard_collision(p)}
    return new_positions


def part1(filepath):
    blizzards, walls = parse_input(filepath)
    walls.add((-1, 1))  # block from going outside valley
    max_r = max(r for r, c in walls)
    max_c = max(c for r, c in walls)
    positions = {(0, 1)}
    minute = 0
    while not any(r == max_r for r, c in positions):
        blizzards = update_blizzards(blizzards, max_r, max_c)
        positions = update_positions(positions, blizzards, walls)
        minute += 1
    return minute


print(part1('inputs/day_24/data.txt'))
