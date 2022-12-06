def part_2(elf_data_filepath):
    max_calories = [0, 0, 0]
    current_calories = 0
    with open(elf_data_filepath) as file:
        lines = [line.strip() for line in file.read().splitlines()]
        for line in lines:
            if not line:
                max_calories.append(current_calories)
                max_calories.sort(reverse=True)
                max_calories.pop()
                current_calories = 0
            else:
                current_calories += int(line)
    return sum(max_calories)


def part_1(elf_data_filepath):
    max_calories = 0
    current_calories = 0
    with open(elf_data_filepath) as file:
        lines = [line.strip() for line in file.read().splitlines()]
        for line in lines:
            current_calories = 0 if not line else current_calories + int(line)
            if current_calories > max_calories:
                max_calories = current_calories
    return max_calories


print(part_1('inputs/day_1/elf_food.txt'))
print(part_2('inputs/day_1/elf_food.txt'))
