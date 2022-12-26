import math


def decimal_to_snafu(decimal):
    result = []
    original_power = math.ceil(math.log(decimal, 5))
    power = math.ceil(math.log(decimal, 5))
    while decimal:
        digit_base_5 = decimal // 5 ** power
        result.append(digit_base_5)
        decimal -= 5 ** power * digit_base_5
        power -= 1
    while len(result) <= original_power:
        result.append(0)
    power = len(result)
    for i in range(1, len(result)):
        digit_1 = result[-i]
        if digit_1 == 4:
            result[-(i + 1)] += 1
            result[-i] = -1
        elif digit_1 == 3:
            result[-(i + 1)] += 1
            result[-i] = -2
        elif digit_1 == 5:
            result[-(i + 1)] += 1
            result[-i] = 0
        power -= 1
    result = ''.join('-' if n == -1 else '=' if n == -2 else str(n) for n in result)
    result = result.lstrip('0')
    return result


def snafu_to_decimal(snafu):
    snafu = [-1 if symbol == '-' else -2 if symbol == '=' else int(symbol) for symbol in snafu]
    return sum((5 ** exponent) * value for exponent, value in enumerate(reversed(snafu)))


def part_1(file_path):
    with open(file_path) as file:
        return sum(snafu_to_decimal(snafu) for snafu in file.read().splitlines())


# print(part_1('inputs/day_25/example_data.txt'))
print(part_1('inputs/day_25/data.txt'))
# print(decimal_to_snafu(33979178787567))
# print(snafu_to_decimal('2=5==21-=25==2201==2'))
# print(decimal_to_snafu(4890))
print(decimal_to_snafu(33979178787567))
print(snafu_to_decimal('2-0==21--=0==2201==2'))
