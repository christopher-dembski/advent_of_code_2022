import re


class MonkeyMap:

    def __init__(self, map_filepath, instructions_filepath):
        self.map = MonkeyMap.parse_map(map_filepath)
        self.instructions = MonkeyMap.parse_instructions(instructions_filepath)
        self.rows = len(self.map)
        self.cols = len(self.map[0])
        self.r, self.c = self.find_starting_position()
        self.dr = 0  # num rows to move
        self.dc = 1  # num cols to move

    @staticmethod
    def parse_map(file_path):
        with open(file_path) as file:
            lines = file.read().splitlines()
            max_length = max(len(line) for line in lines)
            return [list(line) + [' '] * (max_length - len(line)) for line in lines]

    @staticmethod
    def parse_instructions(file_path):
        with open(file_path) as file:
            file_text = file.read().strip()
            instructions = re.findall(r'\d+|L|R', file_text)
            return [int(instruction) if instruction.isnumeric() else instruction for instruction in instructions]

    def find_starting_position(self):
        for r, row in enumerate(self.map):
            for c, symbol in enumerate(row):
                if symbol == '.':  # found empty space
                    return r, c

    def change_direction(self, direction_symbol):
        if direction_symbol == 'R':
            if self.dr == 0 and self.dc == 1:  # East -> South
                self.dr = 1
                self.dc = 0
            elif self.dr == 1 and self.dc == 0:  # South -> West
                self.dr = 0
                self.dc = -1
            elif self.dr == 0 and self.dc == -1:  # West -> North
                self.dr = -1
                self.dc = 0
            else:  # North -> East
                self.dr = 0
                self.dc = 1
        elif direction_symbol == 'L':
            if self.dr == 0 and self.dc == 1:  # East -> North
                self.dr = -1
                self.dc = 0
            elif self.dr == -1 and self.dc == 0:  # North -> West
                self.dr = 0
                self.dc = -1
            elif self.dr == 0 and self.dc == -1:  # West -> South
                self.dr = 1
                self.dc = 0
            else:  # South -> East
                self.dr = 0
                self.dc = 1

    def wrap(self, r, c):
        if r < 0:  # wrap North -> South
            r = self.rows - 1
        elif r == self.rows:  # wrap South -> North
            r = 0
        elif c < 0:  # wrap West -> East
            c = self.cols - 1
        elif c == self.cols:  # wrap East -> West
            c = 0
        return r, c

    def move(self, steps):
        for step in range(steps):
            new_r = self.r + self.dr
            new_c = self.c + self.dc
            new_r, new_c = self.wrap(new_r, new_c)
            while self.map[new_r][new_c] == ' ':  # handle wrapping when leaving map
                new_r += self.dr
                new_c += self.dc
                new_r, new_c = self.wrap(new_r, new_c)
            if self.map[new_r][new_c] == '.':  # if space free (no wall): update
                self.r = new_r
                self.c = new_c

    def simulate(self):
        for instruction in self.instructions:
            if type(instruction) == int:
                self.move(instruction)
            else:  # type(instruction) in ('R', 'L')
                self.change_direction(instruction)
            # print(self.get_state())

    def part1(self):
        self.simulate()
        facing_value = 0 if self.dc == 1 else 1 if self.dr == 1 else 2 if self.dc == -1 else 3  # E0, S1, W2, N3
        return 1000 * (self.r + 1) + 4 * (self.c + 1) + facing_value

    def get_state(self):
        map_copy = [row.copy() for row in self.map]
        map_copy[self.r][self.c] = '^' if self.dr == -1 else '>' if self.dc == 1 else '⌄' if self.dr == 1 else '<'
        return '\n'.join(''.join(row) for row in map_copy) + '\n'


# monkey_map = MonkeyMap('inputs/day_22/example_map.txt', 'inputs/day_22/example_instructions.txt')
# monkey_map = MonkeyMap('inputs/day_22/map.txt', 'inputs/day_22/instructions.txt')
# print(monkey_map.get_state())
# print(monkey_map.part1())
