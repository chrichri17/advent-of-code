NB_TOP_ELVES = 3


def get_max_calories(filepath):
    max_calories = set()
    curr_calories = 0

    with open(filepath) as file:
        for calories in file.readlines():
            if calories == "\n":
                max_calories.add(curr_calories)
                if len(max_calories) > NB_TOP_ELVES:
                    max_calories.remove(min(max_calories))
                curr_calories = 0
            else:
                curr_calories += int(calories.strip())

    return max_calories


def main(filepath):
    max_calories = get_max_calories(filepath)
    print("Part 1:", max(max_calories))
    print("Part 2:", sum(max_calories))
