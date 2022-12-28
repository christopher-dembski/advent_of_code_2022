from operator import add, sub, mul, floordiv


def parse(file_path):
    result = {}
    with open(file_path) as file:
        lines = file.read().splitlines()
        for line in lines:
            name, expression = line.split(':')
            expression = expression.strip()
            if expression.isnumeric():
                result[name] = int(expression)
            else:
                operand_a, operator, operand_b = expression.split()
                operation = {
                    '+': add,
                    '-': sub,
                    '*': mul,
                    '/': floordiv
                }[operator]
                result[name] = (operand_a, operation, operand_b)
    return result


def part_1(file_path):
    def recurse(name):
        expression = monkey_dict[name]
        if type(expression) == int:
            return expression
        operand_a, operation, operand_b = expression
        result = operation(recurse(operand_a), recurse(operand_b))
        monkey_dict[name] = result
        return result

    monkey_dict = parse(file_path)
    return recurse('root')


print(part_1('inputs/day_21/example_data.txt'))
print(part_1('inputs/day_21/data.txt'))
