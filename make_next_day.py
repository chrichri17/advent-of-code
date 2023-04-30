import argparse
import utils

from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    last_year = utils.get_last_year()
    last_day = int(utils.get_last_day(last_year))
    next_day = f"{last_day + 1:02d}"

    parser.add_argument("name")
    parser.add_argument("-y", "--year", default=last_year)
    parser.add_argument("-d", "--day", default=next_day)
    return parser.parse_args()


files = [
    "main.py",
    "data/in.txt",
    "data/test.txt",
    "data/out.txt",
]

main_template = """
def read_inputs(filepath):
    with open(filepath) as file:
        for line in file.readlines():
            yield line.strip()


def main(filepath):
    print("Part 1:", )
    print("Part 2:", )
"""


def main():
    args = parse_args()
    cleaned_name = args.name.replace(" ", "_")

    module_name = f"{args.day}_{cleaned_name}"
    base_dir = Path(f"year_{args.year}") / module_name

    for filename in files:
        p = base_dir / filename
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()

    with open(base_dir / "main.py", "w") as main_file:
        main_file.write(main_template)


if __name__ == "__main__":
    main()
