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
        return f'Node({self.value}, prev={self.previous_node.value}, next={self.next_node.value})'


def parse_input(file_path):
    node_dict = {}
    with open(file_path) as file:
        numbers = iter(int(n) for n in file.read().splitlines())
        head = Node(next(numbers), None, None)
        node_dict[head.value] = head
        previous_node = head
        for n in numbers:
            current_node = Node(n, previous_node, None)
            node_dict[n] = current_node
            previous_node.next_node = current_node
            previous_node = current_node
        head.previous_node = previous_node
        previous_node.next_node = head
        return node_dict, head


def part_1(file_path):
    node_dict, linked_list = parse_input(file_path)
    for number, to_move in node_dict.items():
        if number == 0:
            continue
        to_move.previous_node.next_node = to_move.next_node
        to_move.next_node.previous_node = to_move.previous_node
        current_node = to_move
        if number > 0:
            for step in range(number):
                current_node = current_node.next_node
        else:  # number < 0
            for step in range(abs(number) + 1):
                current_node = current_node.previous_node
        next_node = current_node.next_node
        current_node.next_node = to_move
        to_move.previous_node = current_node
        to_move.next_node = next_node
        next_node.previous_node = to_move
    result = 0
    current_node = linked_list
    while current_node.value != 0:
        current_node = current_node.next_node
    for i in range(1, 3001):
        current_node = current_node.next_node
        if i in (1000, 2000, 3000):
            result += current_node.value
    print(result)


part_1('inputs/day_20/example_data.txt')
