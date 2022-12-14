import re
from itertools import pairwise, chain

PART = 2


class SandCave:

    def __init__(self, file_path):
        self.grid, left_border = self.parse_input(file_path)
        if PART == 2:
            self.grid.append(['.' for _ in range(len(self.grid[0]))])
            self.grid.append(['#' for _ in range(len(self.grid[0]))])
        self.sand_start_r = 0
        self.sand_start_c = 500 - left_border

    def solve(self):
        count = 0
        while self.drop_sand():
            count += 1
        return count if PART == 1 else count + 1

    def drop_sand(self):
        sand_r = self.sand_start_r
        sand_c = self.sand_start_c
        while True:
            if PART == 2:
                if sand_c == len(self.grid[0]) - 1:
                    self.add_colum_right()
                elif sand_c == 0:
                    self.add_column_left()
            if self.within_grid(sand_r + 1, sand_c) and self.grid[sand_r + 1][sand_c] == '.':
                sand_r += 1
            elif self.within_grid(sand_r + 1, sand_c - 1) and self.grid[sand_r + 1][sand_c - 1] == '.':
                sand_r += 1
                sand_c -= 1
            elif self.within_grid(sand_r + 1, sand_c + 1) and self.grid[sand_r + 1][sand_c + 1] == '.':
                sand_r += 1
                sand_c += 1
            else:
                if PART == 1:
                    if sand_c == 0 or sand_c == len(self.grid[0]) - 1 or sand_r == len(self.grid) - 1:
                        return False
                    else:
                        self.grid[sand_r][sand_c] = 'o'
                        return True
                else:  # PART == 2
                    if sand_r == 0:
                        return False
                    else:
                        self.grid[sand_r][sand_c] = 'o'
                        return True

    def add_colum_right(self):
        for row in self.grid:
            row.append('.')
        self.grid[-1][-1] = '#'

    def add_column_left(self):
        for r, row in enumerate(self.grid):
            self.grid[r] = ['.'] + row
        self.grid[-1][0] = '#'
        self.sand_start_c += 1

    def within_grid(self, r, c):
        return 0 <= r < len(self.grid) and 0 <= c < len(self.grid[0])

    def display(self):
        print('\n'.join(''.join(ch for ch in line) for line in self.grid))

    @staticmethod
    def parse_input(file_path):
        with open(file_path) as file:
            lines = file.read().splitlines()
            all_paths = []
            for line in lines:
                paths = SandCave.parse_line(line)
                all_paths.append(paths)
            left_border = min(min(c for c, r in chain(*all_paths)), 500)
            right_border = max(max(c for c, r in chain(*all_paths)), 500)
            top_border = 0  # sand start at 0
            bottom_border = max(r for c, r in chain(*all_paths))
            grid = [['.' for c in range(left_border, right_border + 1)]
                    for r in range(top_border, bottom_border + 1)]
            SandCave.populate_grid(all_paths, grid, left_border)
            return grid, left_border

    @staticmethod
    def populate_grid(all_paths, grid, left_border):
        for paths in all_paths:
            for (start_c, start_r), (stop_c, stop_r) in pairwise(paths):
                for r in range(min(start_r, stop_r), max(start_r, stop_r) + 1):
                    for c in range(min(start_c, stop_c), max(start_c, stop_c) + 1):
                        grid[r][c - left_border] = '#'

    @staticmethod
    def parse_line(line):
        paths = re.split(' -> ', line)
        paths = [path.split(',') for path in paths]
        paths = [(int(start), int(stop)) for start, stop in paths]
        return paths


# note: working for example input but not real data
sand_cave = SandCave('inputs/day_14/data.txt')
print(sand_cave.solve())
sand_cave.display()
