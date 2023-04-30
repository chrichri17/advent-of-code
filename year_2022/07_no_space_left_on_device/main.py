from collections import defaultdict


def update_path(curr_path, dir_name):
    if dir_name == "..":
        # pop is legal here given the inputs
        return curr_path.pop()

    if not dir_name.endswith("/"):
        dir_name += "/"
    curr_path.append(dir_name)


def compute_folders_size(filepath):
    folders_size = defaultdict(int)
    current_path = []

    for line in open(filepath).read().splitlines():
        if line.startswith("$ ls"):
            # List directory : noop
            continue
        if line.startswith("$ cd"):
            # New directory : update the current path
            update_path(current_path, line[5:])
        else:
            size, name = line.split()
            path = "".join(current_path)
            if size == "dir":
                # Initialize the size of the subdirectory
                folders_size[path + name + "/"] = 0
            else:
                # Update the current directory size
                folders_size[path] += int(size)

    # Aggreagation : propagate subfolder sizes to their parents
    for folder in folders_size:
        for subfolder in folders_size:
            if subfolder.startswith(folder) and folder != subfolder:
                folders_size[folder] += folders_size[subfolder]

    return folders_size


MAX_SIZE = 100_000


def part1(filepath):
    folders_size = compute_folders_size(filepath)
    # Get sum of folders having size < MAX_SIZE
    return sum(filter(lambda size: size < MAX_SIZE, folders_size.values()))


TOTAL_DISK_SPACE = 70_000_000

REQUIRED_FREE_SPACE = 30_000_000


def part2(filepath):
    folders_size = compute_folders_size(filepath)
    total_space_used = folders_size.get("/")
    free_space_on_disk = TOTAL_DISK_SPACE - total_space_used
    needed_space = REQUIRED_FREE_SPACE - free_space_on_disk

    # Get folders with size >= needed_space
    filter_fn = lambda f: folders_size[f] >= needed_space
    deletable_folders = list(filter(filter_fn, folders_size))

    return min(map(lambda f: folders_size[f], deletable_folders))


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
