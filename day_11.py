import re
from operator import add, mul


class Monkey:
    monkeys = []
    next_id = 0

    @classmethod
    def print_state(cls):
        print('State')
        for monkey in cls.monkeys:
            print(monkey.items)

    def __init__(self, starting_items, operand1, operator, operand2, test_divisor, true_throw, false_throw):
        self.id = Monkey.next_id
        Monkey.next_id += 1
        self.items = starting_items
        self.operand1 = operand1
        self.operator = operator
        self.operand2 = operand2
        self.test_divisor = test_divisor
        self.true_throw = true_throw
        self.false_throw = false_throw
        self.inspected_items = 0

    def inspect(self, item_index):
        item = self.items[item_index]
        operand1 = item if self.operand1 == 'old' else self.operand1
        operand2 = item if self.operand2 == 'old' else self.operand2
        operation = add if self.operator == '+' else mul
        self.items[item_index] = operation(operand1, operand2)  # become more worried as monkey inspects
        self.items[item_index] //= 3  # monkey bored with item, worry drops
        self.inspected_items += 1

    def throw(self, item_index):
        item = self.items[item_index]
        throw_to = self.false_throw if item % self.test_divisor else self.true_throw
        Monkey.monkeys[throw_to].items.append(item)

    def throw_items(self):
        for index in range(len(self.items)):
            self.inspect(index)
            self.throw(index)
        self.items.clear()

    def __repr__(self):
        return f'Monkey {self.id}:\n' \
               f'   Current items: {self.items}\n' \
               f'   Operation: new = {self.operand1} {self.operator} {self.operand2}\n' \
               f'   Test: divisible by {self.test_divisor}\n' \
               f'       If true: throw to monkey {self.true_throw}\n' \
               f'       If false: throw to monkey {self.false_throw}\n'


def parse_input(file_path):
    with open(file_path) as file:
        sections = re.split(r'\n{2}', file.read())
        return [parse_section(section_text) for section_text in sections]


def parse_section(section_text):
    lines = section_text.splitlines()
    starting_items = [int(worry_level) for worry_level in re.findall(r'\d+', lines[1])]
    operand1, operator, operand2 = re.findall(r'(\d+|old) (\+|\*) (\d+|old)', lines[2]).pop()
    if operand1 != 'old':
        operand1 = int(operand1)
    if operand2 != 'old':
        operand2 = int(operand2)
    test_divisor = int(re.search(r'\d+', lines[3]).group(0))
    true_throw = int(re.search(r'\d+', lines[4]).group(0))
    false_throw = int(re.search(r'\d+', lines[5]).group(0))
    return Monkey(starting_items,
                  operand1, operator, operand2,
                  test_divisor, true_throw, false_throw)


def solve(file_path, part):
    Monkey.monkeys = parse_input(file_path)
    for round_number in range(20 if part == 1 else 10000):
        for monkey in Monkey.monkeys:
            monkey.throw_items()
    items_inspected = sorted(monkey.inspected_items for monkey in Monkey.monkeys)
    return items_inspected[-1] * items_inspected[-2]


print(solve('inputs/day_11/data.txt', 1))
