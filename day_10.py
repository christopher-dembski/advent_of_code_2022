SPECIAL_CYCLES = (20, 60, 100, 140, 180, 220)


def parse_input(file_path):
    with open(file_path) as file:
        instructions = file.read().splitlines()
        instructions = [line.split() for line in instructions]
        return [('noop', None) if instruction[0] == 'noop' else ('addx', int(instruction[1]))
                for instruction in instructions]


def is_special_cycle(cycle):
    return not ((cycle - 20) % 40)


def solve_part_1(file_path):
    signal_strengths = []
    register = 1
    cycle = 0
    instructions = parse_input(file_path)
    for opcode, value in instructions:
        if opcode == 'noop':
            cycle += 1
            if cycle in SPECIAL_CYCLES:
                signal_strengths.append(cycle * register)
        else:  # opcode == 'addx'
            for add_cycle in range(2):
                cycle += 1
                if cycle in SPECIAL_CYCLES:
                    signal_strengths.append(cycle * register)
            register += value
    return sum(signal_strengths)


print(solve_part_1('inputs/day_10/data.txt'))
