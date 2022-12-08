from functools import cached_property

TOTAL_DISK_SPACE = 70000000
REQUIRED_SPACE = 30000000


class Node:

    def __init__(self, name, parent_directory):
        self.name = name
        self.parent_directory = parent_directory


class Directory(Node):

    def __init__(self, name, parent_directory, children):
        super().__init__(name, parent_directory)
        self.children = children

    @cached_property  # requires the size not to change after property accessed (i.e. no sub-directories/files added)
    def size(self):
        return sum(child.size for child in self.children.values())

    def str_rep(self, level=0):
        result = f'Directory({self.name})'
        for child in self.children.values():
            result += '\n' + '    ' * level + child.str_rep(level + 1)
        return result


class File(Node):

    def __init__(self, name, size, parent_directory):
        super().__init__(name, parent_directory)
        self.size = size

    def str_rep(self, level=0):
        return '    ' * level + f'File({self.name}, {self.size})'


def get_tokens(data_file_path):
    with open(data_file_path) as file:
        return [line.split() for line in file.read().splitlines()]


def build_tree(data_file_path):
    root = Directory('/', None, {})
    current_directory = root
    for tokens in get_tokens(data_file_path):
        if tokens[0] == '$':
            if tokens[1] == 'cd':
                to_directory = tokens[2]
                if to_directory == '/':
                    current_directory = root
                elif to_directory == '..':
                    current_directory = current_directory.parent_directory
                else:
                    if to_directory in current_directory.children:
                        current_directory = current_directory.children[to_directory]
                    else:
                        current_directory.children[to_directory] = Directory(to_directory, current_directory, {})
        elif tokens[0] == 'dir':
            dir_name = tokens[1]
            if dir_name not in current_directory.children:
                current_directory.children[dir_name] = Directory(dir_name, current_directory, {})
        else:  # file
            file_size = int(tokens[0])
            file_name = tokens[1]
            if file_name not in current_directory.children:
                current_directory.children[file_name] = File(file_name, file_size, current_directory)
    return root


def part_1(data_file_path):
    root = build_tree(data_file_path)
    total = 0
    to_check = [root]
    while to_check:
        node = to_check.pop()
        if type(node) == File:
            continue
        if node.size <= 100000:
            total += node.size
        to_check.extend(node.children.values())
    return total


def directory_size_to_delete(root, size_to_free):
    smallest_size = root.size
    to_check = [root]
    while to_check:
        node = to_check.pop()
        if type(node) == File:
            continue
        if size_to_free <= node.size < smallest_size:
            smallest_size = node.size
        to_check.extend(node.children.values())
    return smallest_size


def part_2(data_file_path):
    root = build_tree(data_file_path)
    space_used = root.size
    space_remaining = TOTAL_DISK_SPACE - space_used
    space_to_free = REQUIRED_SPACE - space_remaining
    return directory_size_to_delete(root, space_to_free)


print(part_1('inputs/day_7/terminal_output.txt'))  # 1306611
print(part_2('inputs/day_7/terminal_output.txt'))  # 13210366
