STRATEGY_TOKENS_DICT = {'A': 'rock', 'B': 'paper', 'C': 'scissors', 'X': 'rock', 'Y': 'paper', 'Z': 'scissors'}

POINTS_FOR_CHOICE_DICT = {'rock': 1, 'paper': 2, 'scissors': 3}

POINTS_FOR_OUTCOME_DICT = {
    ('rock', 'rock'): 3, ('rock', 'paper'): 6, ('rock', 'scissors'): 0,
    ('paper', 'rock'): 0, ('paper', 'paper'): 3, ('paper', 'scissors'): 6,
    ('scissors', 'rock'): 6, ('scissors', 'paper'): 0, ('scissors', 'scissors'): 3,
}

# [their_choice][outcome_code] -> your_choice
# outcome_codes: X lose | Y draw | Z win
DETERMINE_CHOICE_DICT = {
    'rock': {'X': 'scissors', 'Y': 'rock', 'Z': 'paper'},
    'paper': {'X': 'rock', 'Y': 'paper', 'Z': 'scissors'},
    'scissors': {'X': 'paper', 'Y': 'scissors', 'Z': 'rock'}
}


def solve(strategy_data_filepath, part=1):
    choices = parse_input(strategy_data_filepath, part)
    points = 0
    for their_choice, your_choice in choices:
        points += POINTS_FOR_CHOICE_DICT[your_choice]
        points += POINTS_FOR_OUTCOME_DICT[(their_choice, your_choice)]
    return points


def parse_input(strategy_data_filepath, part):
    with open(strategy_data_filepath) as file:
        lines = file.read().splitlines()
        tokens = [line.split() for line in lines]
        if part == 1:
            return [(STRATEGY_TOKENS_DICT[token_a], STRATEGY_TOKENS_DICT[token_b]) for token_a, token_b in tokens]
        else:
            return [(STRATEGY_TOKENS_DICT[token_a], DETERMINE_CHOICE_DICT[STRATEGY_TOKENS_DICT[token_a]][token_b])
                    for token_a, token_b in tokens]


print(solve('inputs/day_2/strategy_data.txt', part=1))
print(solve('inputs/day_2/strategy_data.txt', part=2))
