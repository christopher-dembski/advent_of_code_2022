class Coordinate:

    def __init__(self, r, c):
        self.r = r
        self.c = c

    def distance(self, other):
        return max(abs(self.r - other.r), abs(self.c - other.c))

    def follow(self, leader):
        delta_r = leader.r - self.r
        delta_c = leader.c - self.c
        if abs(delta_r) < 2 and abs(delta_c) < 2:
            return Coordinate(0, 0)
        move = Coordinate(0, 0)
        if delta_r > 0:
            move.r = 1
        elif delta_r < 0:
            move.r = -1
        if delta_c > 0:
            move.c = 1
        elif delta_c < 0:
            move.c = -1
        return move

    def __add__(self, other):
        return Coordinate(self.r + other.r, self.c + other.c)

    def __repr__(self):
        return f'Coordinate({self.r}, {self.c})'


class Bridge:
    DIRECTION_VECTORS = {
        'U': Coordinate(-1, 0),
        'R': Coordinate(0, 1),
        'D': Coordinate(1, 0),
        'L': Coordinate(0, -1)
    }

    def __init__(self, data_file_path, num_knots=10):
        self.instructions = Bridge.parse_directions(data_file_path)
        self.head = Coordinate(0, 0)
        self.tail = Coordinate(0, 0)
        self.tail_visited = {(0, 0)}
        self.knots = [Coordinate(0, 0) for _ in range(num_knots)]

    @staticmethod
    def parse_directions(data_file_path):
        with open(data_file_path) as file:
            lines = file.read().splitlines()
            directions_distances = [line.split() for line in lines]
            return [(direction, int(distance)) for direction, distance in directions_distances]

    def simulate_part_1(self):
        for direction, distance in self.instructions:
            direction_vector = Bridge.DIRECTION_VECTORS[direction]
            for move in range(distance):
                prev_head = Coordinate(self.head.r, self.head.c)
                self.head += direction_vector
                if self.head.distance(self.tail) > 1:
                    self.tail = prev_head
                self.tail_visited.add((self.tail.r, self.tail.c))
        return len(self.tail_visited)

    def simulate_part_2(self):
        for direction, distance in self.instructions:
            direction_vector = Bridge.DIRECTION_VECTORS[direction]
            for move in range(distance):
                for i, knot in enumerate(self.knots):
                    if i == 0:  # lead-knot moves one space
                        self.knots[i] += direction_vector
                    else:
                        preceding_knot = self.knots[i - 1]
                        to_move = knot.follow(preceding_knot)
                        self.knots[i] = knot + to_move
                tail = self.knots[-1]
                self.tail_visited.add((tail.r, tail.c))
        return len(self.tail_visited)


bridge = Bridge('inputs/day_9/data.txt')
# print(bridge.simulate_part_1())
print(bridge.simulate_part_2())
