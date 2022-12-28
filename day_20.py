class Node:

    def __init__(self, value, previous_node, next_node):
        self.value = value
        self.previous_node = previous_node
        self.next_node = next_node

    def display(self):
        numbers = [self.value]
        current = self.next_node
        while id(current) != id(self):
            numbers.append(current.value)
            current = current.next_node
        print(' -> '.join(str(n) for n in numbers))

    def __repr__(self):
        return f'Node(value={self.value}, prev={self.previous_node.value}, next={self.next_node.value})'


def parse_input(file_path):
    nodes = []
    with open(file_path) as file:
        numbers = iter(int(n) for n in file.read().splitlines())
        head = Node(next(numbers), None, None)
        nodes.append(head)
        previous_node = head
        for n in numbers:
            current_node = Node(n, previous_node, None)
            nodes.append(current_node)
            previous_node.next_node = current_node
            previous_node = current_node
        head.previous_node = previous_node
        previous_node.next_node = head
        return nodes


def mix(nodes):  # MUTATES: linked_list
    for to_move in nodes:
        if to_move.value == 0:
            continue
        to_move.previous_node.next_node = to_move.next_node
        to_move.next_node.previous_node = to_move.previous_node
        current_node = to_move
        if to_move.value > 0:
            for step in range(to_move.value):
                current_node = current_node.next_node
        else:  # to_move.value < 0
            for step in range(abs(to_move.value) + 1):
                current_node = current_node.previous_node
        next_node = current_node.next_node
        current_node.next_node = to_move
        to_move.previous_node = current_node
        to_move.next_node = next_node
        next_node.previous_node = to_move


def sum_grove_coordinates(nodes):
    print(nodes)
    result = 0
    current_node = nodes[0]
    while current_node.value != 0:
        current_node = current_node.next_node
    for i in range(1, 3001):
        current_node = current_node.next_node
        if i in (1000, 2000, 3000):
            result += current_node.value
    return result


def part_1(file_path):
    nodes = parse_input(file_path)
    mix(nodes)  # MUTATION: linked_list
    return sum_grove_coordinates(nodes)


class Wrapper:

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self is other

    def __repr__(self):
        return f'Wrapper({self.value})'


def parse_part_2(file_path):
    with open(file_path) as file:
        return [Wrapper(int(n)) for n in file.read().splitlines()]


def mix_part_2(numbers_original_order, numbers):  # MUTATES: numbers
    for wrapped_number in numbers_original_order:
        original_index = numbers.index(wrapped_number)
        numbers[original_index] = None
        insertion_index = (original_index + wrapped_number.value) % len(numbers)
        if wrapped_number.value > 0:
            insertion_index += 1
        numbers.insert(insertion_index, wrapped_number)
        numbers.remove(None)


def sum_grove_coordinates_2(numbers):
    print(numbers)
    i = 0
    while numbers[i].value != 0:
        i += 1
        if i == len(numbers):
            i = 0
    one_thousandth = numbers[(i + 1000) % len(numbers)].value
    two_thousandth = numbers[(i + 2000) % len(numbers)].value
    three_thousandth = numbers[(i + 3000) % len(numbers)].value
    return one_thousandth + two_thousandth + three_thousandth


def part_2(file_path):
    numbers_original_order = parse_part_2(file_path)
    numbers = numbers_original_order.copy()
    mix_part_2(numbers_original_order, numbers)  # MUTATION: numbers
    return sum_grove_coordinates_2(numbers)


print(part_1('inputs/day_20/example_data.txt'))  # should match
print(part_2('inputs/day_20/example_data.txt'))  # should match