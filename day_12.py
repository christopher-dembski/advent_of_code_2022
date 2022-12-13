import string

ELEVATION_DICT = {**{letter: i for i, letter in enumerate(string.ascii_lowercase)}, **{'S': -1, 'E': 26}}


def parse_input(file_path):
    with open(file_path) as file:
        lines = file.read().splitlines()
        return [[ELEVATION_DICT[ch] if ch in ELEVATION_DICT else ch for ch in line] for line in lines]


def get_starting_position(grid):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == -1:
                return r, c


def within_grid(r, c, grid):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def get_neighbours(input_r, input_c, grid):
    adjacent = ((input_r - 1, input_c), (input_r, input_c + 1), (input_r + 1, input_c), (input_r, input_c - 1))
    return [(r, c) for r, c in adjacent if within_grid(r, c, grid)]


def bfs(start_r, start_c, grid):
    seen = {(start_r, start_c)}
    to_check = [(start_r, start_c)]
    path_length = 0
    while to_check:
        next_to_check = []
        path_length += 1
        for origin_r, origin_c in to_check:
            adjacent = get_neighbours(origin_r, origin_c, grid)
            for adj_r, adj_c in adjacent:
                current_height = grid[origin_r][origin_c]
                adj_height = grid[adj_r][adj_c]
                if (adj_r, adj_c) in seen or not within_grid(adj_r, adj_c, grid) or adj_height - current_height > 1:
                    continue
                if grid[adj_r][adj_c] == 26:
                    return path_length
                else:
                    seen.add((adj_r, adj_c))
                    next_to_check.append((adj_r, adj_c))
        to_check.clear()
        to_check.extend(next_to_check)


def solve_part_1(file_path):
    grid = parse_input(file_path)
    start_r, start_c = get_starting_position(grid)
    return bfs(start_r, start_c, grid)


def find_positions_at_elevation_a(grid):
    return [(r, c) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] in (-1, 0)]


def solve_part_2(file_path):
    grid = parse_input(file_path)
    positions_elevation_a = find_positions_at_elevation_a(grid)
    path_lengths = [bfs(r, c, grid) for r, c in positions_elevation_a]
    return min(path_length for path_length in path_lengths if path_length is not None)


print(solve_part_2('inputs/day_12/data.txt'))
