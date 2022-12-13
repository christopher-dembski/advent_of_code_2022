import re
import json


class WrongOrder(Exception):
    pass


class RightOrder(Exception):
    pass


def parse_input(file_path):
    with open(file_path) as file:
        pairs = re.split('\n\n', file.read())
        return [parse_pair(pair_string) for pair_string in pairs]


def parse_pair(pair_string):
    packet1, packet2 = pair_string.split('\n')
    return json.loads(packet1), json.loads(packet2)


def compare(packet1, packet2):
    for left, right in zip(packet1, packet2):
        if type(left) == int and type(right) == int:
            if left < right:
                raise RightOrder
            elif left > right:
                raise WrongOrder
        elif type(left) == list and type(right) == list:
            compare(left, right)
        elif type(left) == int and type(right) == list:
            compare([left], right)
        elif type(left) == list and type(right) == int:
            compare(left, [right])
    if len(packet1) < len(packet2):
        raise RightOrder
    elif len(packet1) > len(packet2):
        raise WrongOrder


def part1(file_path):
    pairs = parse_input(file_path)
    result = 0
    for i, (packet1, packet2) in enumerate(pairs):
        try:
            compare(packet1, packet2)
        except RightOrder:
            result += i + 1
        except WrongOrder:
            pass
    return result


def parse_part2(file_path):
    with open(file_path) as file:
        lines = file.read().splitlines()
        return [json.loads(line) for line in lines if line]


def correct_order(packet1, packet2):
    try:
        compare(packet1, packet2)
    except RightOrder:
        return True
    except WrongOrder:
        return False


def part2(file_path):
    packets = parse_part2(file_path)
    packets.append([[2]])
    packets.append([[6]])
    for stop in range(len(packets) - 1, 1, -1):
        for i in range(stop):
            packet1 = packets[i]
            packet2 = packets[i + 1]
            if not correct_order(packet1, packet2):
                packets[i] = packet2
                packets[i + 1] = packet1
    divider_packet_indexes = [i + 1 for i, packet in enumerate(packets) if packet in ([[2]], [[6]])]
    return divider_packet_indexes[0] * divider_packet_indexes[1]


print(part2('inputs/day_13/data.txt'))
