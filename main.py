import argparse
import sys
from contextlib import redirect_stdout
from glob import glob
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
    if module is None:
        print(f"Module for year {args.year} and day {args.day} not found.")
        return
    data_dir = Path(module.__file__).parent / "data"

    if args.input == "all":
        inputs = glob("test*.txt", root_dir=data_dir)
        inputs.append("in.txt")
    else:
        inputs = glob(f"{args.input}*.txt", root_dir=data_dir)

    cout = open(data_dir / "out.txt", "w") if args.save else sys.stdout

    with redirect_stdout(cout):
        for input_file in inputs:
            print(input_file)
            print("-" * len(input_file))
            module.main(data_dir / input_file)
            print()


if __name__ == "__main__":
    main()
