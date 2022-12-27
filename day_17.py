from itertools import cycle, chain


class Cave:

    def __init__(self, file_path, part):
        self.part = part
        jet_pattern = self.parse_jet_pattern(file_path)
        self.jet_pattern = cycle(jet_pattern)
        self.rock_cycle = cycle((1, 2, 3, 4, 5))
        self.fallen = set()
        self.falling = set()
        self.max_y = 0

    @staticmethod
    def parse_jet_pattern(file_path):
        with open(file_path) as file:
            return file.read().strip()

    def init_next_rock(self):
        rock_number = next(self.rock_cycle)
        {
            1: self.init_rock_1,
            2: self.init_rock_2,
            3: self.init_rock_3,
            4: self.init_rock_4,
            5: self.init_rock_5
        }[rock_number]()

    def init_rock_1(self):
        self.falling = {(3, self.max_y + 4), (4, self.max_y + 4), (5, self.max_y + 4), (6, self.max_y + 4)}

    def init_rock_2(self):
        self.falling = {(4, self.max_y + 6),
                        (3, self.max_y + 5), (4, self.max_y + 5), (5, self.max_y + 5),
                        (4, self.max_y + 4)}

    def init_rock_3(self):
        self.falling = {(5, self.max_y + 6),
                        (5, self.max_y + 5),
                        (3, self.max_y + 4), (4, self.max_y + 4), (5, self.max_y + 4)}

    def init_rock_4(self):
        self.falling = {(3, self.max_y + 7),
                        (3, self.max_y + 6),
                        (3, self.max_y + 5),
                        (3, self.max_y + 4)}

    def init_rock_5(self):
        self.falling = {(3, self.max_y + 5), (4, self.max_y + 5),
                        (3, self.max_y + 4), (4, self.max_y + 4)}

    def jet_push(self):
        direction_symbol = next(self.jet_pattern)
        if direction_symbol == '<':
            if all(x > 1 and (x - 1, y) not in self.fallen for x, y in self.falling):
                self.falling = {(x - 1, y) for x, y in self.falling}
        else:  # direction symbol == '>'
            if all(x < 7 and (x + 1, y) not in self.fallen for x, y in self.falling):
                self.falling = {(x + 1, y) for x, y in self.falling}

    def fall(self):
        self.falling = {(x, y - 1) for x, y in self.falling}

    def simulate(self):
        for rock_number in range(2022 if self.part == 1 else 1000000000000):
            self.init_next_rock()
            self.jet_push()
            while not (any(y == 1 for x, y in self.falling) or any((x, y - 1) in self.fallen for x, y in self.falling)):
                self.fall()
                self.jet_push()
            self.max_y = max(self.max_y, *[y for x, y in self.falling])
            self.fallen |= self.falling
            self.falling.clear()
        return self.max_y

    def display(self):
        grid = [['@' if (x, y) in self.falling else '#' if (x, y) in self.fallen else '.' for x in range(1, 8)]
                for y in range(self.max_y, 0, -1)]
        print('\n'.join(''.join(char for char in row) for row in grid), end='\n\n')


cave = Cave('inputs/day_17/example_data.txt', part=1)
print(cave.simulate())
