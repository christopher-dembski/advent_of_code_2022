from functools import reduce


def parse_input(file_path):
    with open(file_path) as file:
        return [[int(height) for height in line] for line in file.read().splitlines()]


class Forest:

    def __init__(self, trees):
        self.trees = trees
        self.height = len(trees)
        self.width = len(trees[0])
        self.visibility_grid = [[self.check_visibility(r, c) for c in range(self.width)] for r in range(self.height)]

    def solve_part1(self):
        return sum(self.visibility_grid[r][c] for r in range(self.height) for c in range(self.width))

    def solve_part2(self):
        return max(self.scenic_score(r, c) for r in range(self.height) for c in range(self.width))

    def check_visibility(self, target_r, target_c):
        return any((self.north_visibility(target_r, target_c),
                    self.east_visibility(target_r, target_c),
                    self.south_visibility(target_r, target_c),
                    self.west_visibility(target_r, target_c)))

    def north_visibility(self, target_r, target_c):
        height = self.trees[target_r][target_c]
        return all(self.trees[r][target_c] < height for r in range(target_r))

    def east_visibility(self, target_r, target_c):
        height = self.trees[target_r][target_c]
        return all(self.trees[target_r][c] < height for c in range(target_c + 1, self.width))

    def south_visibility(self, target_r, target_c):
        height = self.trees[target_r][target_c]
        return all(self.trees[r][target_c] < height for r in range(target_r + 1, self.height))

    def west_visibility(self, target_r, target_c):
        height = self.trees[target_r][target_c]
        return all(self.trees[target_r][c] < height for c in range(target_c))

    def scenic_score(self, initial_r, initial_c):
        if initial_r == 0 or initial_c == 0 or initial_r == self.height - 1 or initial_c == self.width - 1:
            return 0
        tree_house_height = self.trees[initial_r][initial_c]
        viewing_distances = []
        for dr, dc in ((-1, 0), (0, 1), (1, 0), (0, -1)):  # N-E-S-W
            r = initial_r + dr
            c = initial_c + dc
            viewing_distance = 1
            while self.in_bounds(r + dr, c + dc) and self.trees[r][c] < tree_house_height:
                r += dr
                c += dc
                viewing_distance += 1
            viewing_distances.append(viewing_distance)
        return reduce(lambda total, distance: total * distance, viewing_distances)

    def in_bounds(self, r, c):
        return 0 <= r < self.height and 0 <= c < self.width


forest = Forest(parse_input('inputs/day_8/data.txt'))
print(forest.solve_part1())
print(forest.solve_part2())
