import argparse
import sys
from contextlib import redirect_stdout
from pathlib import Path

import utils


def parse_args():
    parser = argparse.ArgumentParser()
    last_year = utils.get_last_year()
    last_day = utils.get_last_day(last_year)

    parser.add_argument("-y", "--year", default=last_year)
    parser.add_argument("-d", "--day", default=last_day)
    parser.add_argument("-i", "--input", default="all", choices="in test all".split())
    parser.add_argument("--save", action="store_true", default=False)
    return parser.parse_args()


def main():
    args = parse_args()
    module = utils.get_module(args.year, args.day)
    data_dir = Path(module.__file__).parent / "data"

    if args.input == "all":
        inputs = ["test.txt", "in.txt"]
    else:
        inputs = [f"{args.input}.txt"]

    cout = open(data_dir / "out.txt", "w") if args.save else sys.stdout

    with redirect_stdout(cout):
        for input_file in inputs:
            print(input_file)
            print("-" * len(input_file))
            module.main(data_dir / input_file)
            print()


if __name__ == "__main__":
    main()
