def solve(file_path, package_marker_length):
    with open(file_path) as file:
        data = file.read().strip()
        for i, ch in enumerate(data):
            if len(set(data[i - package_marker_length + 1:i + 1])) == package_marker_length:
                return i + 1


print(solve('inputs/day_6/data.txt', 4))
print(solve('inputs/day_6/data.txt', 14))
