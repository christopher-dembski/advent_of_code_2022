SPECIAL_CYCLES = (20, 60, 100, 140, 180, 220)


def parse_input(file_path):
    with open(file_path) as file:
        instructions = file.read().splitlines()
        instructions = [line.split() for line in instructions]
        return [('noop', None) if instruction[0] == 'noop' else ('addx', int(instruction[1]))
                for instruction in instructions]


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


def update_crt(register, cycle, crt):  # MUTATION: crt
    r = (cycle - 1) // 40
    sprite_positions = [c for c in (register - 1, register, register + 1) if 0 <= c < 40]
    column_being_drawn = (cycle - 1) % 40
    if column_being_drawn in sprite_positions:
        crt[r][column_being_drawn] = '#'
    else:
        crt[r][column_being_drawn] = ' '  # easier to see resulting letters than '.'


def solve_part_2(file_path):
    crt = [['-' for c in range(40)] for r in range(6)]
    register = 1
    cycle = 0
    instructions = parse_input(file_path)
    for opcode, value in instructions:
        if opcode == 'noop':
            cycle += 1
            update_crt(register, cycle, crt)  # MUTATION: crt
        else:  # opcode == 'addx'
            for add_cycle in range(2):
                cycle += 1
                update_crt(register, cycle, crt)  # MUTATION: crt
            register += value
    return '\n'.join(''.join(row) for row in crt)


print(solve_part_1('inputs/day_10/data.txt'))
print(solve_part_2('inputs/day_10/data.txt'))
