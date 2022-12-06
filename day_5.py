import csv
import string


def solve(moves_filename, stacks_filename, part):
    moves = parse_move_list(moves_filename)
    stacks = parse_stacks_dict(stacks_filename)
    for number_to_move, from_stack, to_stack in moves:
        if part == 1:
            for mv in range(number_to_move):
                letter_to_move = stacks[from_stack].pop()
                stacks[to_stack].append(letter_to_move)
        else:  # part == 2
            letters_to_move = stacks[from_stack][-number_to_move:]
            for _ in range(number_to_move):
                stacks[from_stack].pop()
            stacks[to_stack].extend(letters_to_move)
    return ''.join(stack[-1] for stack in stacks.values() if stack)


# output [(number_to_move, from_stack, to_stack), ...] | ex. [(3, 1, 5), ...]
def parse_move_list(filename):
    result = []
    with open(filename) as file:
        reader = csv.reader(file.readlines(), delimiter=' ')
        for line in reader:
            move, number, from_, from_stack, to, to_stack = line
            result.append((int(number), int(from_stack), int(to_stack)))

    return result


# output: {stack_number: stack_of_letters, ...} | ex {1: ['A', 'G', 'X'], ...}
def parse_stacks_dict(file_name):
    with open(file_name) as file:
        rows = file.read().splitlines()
        column_indexes = {i for i, n in enumerate(rows.pop()) if n in string.digits}  # indexes where crates stacked
        # change from rows to columns, and only include columns with stacks of crates
        columns = [[rows[r][c] for r in range(len(rows))] for c in range(len(rows[0])) if c in column_indexes]
        # reverse columns so top letter is at end of list (i.e. top of the stack) and remove empty positions
        columns = [[char for char in reversed(col) if char in string.ascii_uppercase] for col in columns]
        return {i + 1: stack for i, stack in enumerate(columns)}  # +1 b/c crate columns are indexed starting at 1


print(solve('inputs/day_5/moves.txt', 'inputs/day_5/stacks.txt', part=1))
print(solve('inputs/day_5/moves.txt', 'inputs/day_5/stacks.txt', part=2))
