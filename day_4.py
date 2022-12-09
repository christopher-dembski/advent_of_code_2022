import re


class Range:

    def __init__(self, start, stop):
        self.start = start
        self.stop = stop  # inclusive

    def fully_contains(self, other):
        return self.start <= other.start and self.stop >= other.stop

    def overlaps(self, other):
        return self.start <= other.stop <= self.stop or \
               self.start <= other.start <= self.stop or \
               other.fully_contains(self)

    def __repr__(self):
        return f'Range({self.start}, {self.stop})'


def parse_input(file_path):
    with open(file_path) as file:
        parsed = [line for line in file.read().splitlines()]
        parsed = [re.split('-|,', line) for line in parsed]
        parsed = [map(int, number_list) for number_list in parsed]
        return [(Range(start1, stop1), Range(start2, stop2)) for start1, stop1, start2, stop2 in parsed]


def solve_part_1(file_path):
    range_pairs = parse_input(file_path)
    return sum(range1.fully_contains(range2) or range2.fully_contains(range1) for range1, range2 in range_pairs)


def solve_part_2(file_path):
    range_pairs = parse_input(file_path)
    return sum(range1.overlaps(range2) for range1, range2 in range_pairs)


print(solve_part_1('inputs/day_4/data.txt'))
print(solve_part_2('inputs/day_4/data.txt'))
