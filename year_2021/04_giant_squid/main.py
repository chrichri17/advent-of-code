# https://adventofcode.com/2021/day/04
from dataclasses import dataclass


@dataclass
class Cell:
    value: int
    marked: bool = False


@dataclass
class Board:
    rows: list[list[Cell]]

    def mark_cells(self, num):
        for row in self.rows:
            for cell in row:
                if cell.value == num:
                    cell.marked = True

    def is_winning(self):
        return any(all(cell.marked for cell in row) for row in self.rows) or any(
            all(cell.marked for cell in col) for col in zip(*self.rows)
        )

    def sum_unmarked(self):
        return sum(cell.value for row in self.rows for cell in row if not cell.marked)

    def __repr__(self) -> str:
        return "\n".join(
            " ".join(f"{cell.value:2d}" for cell in row) for row in self.rows
        )


def read_inputs(filepath):
    with open(filepath) as file:
        nums = list(map(int, file.readline().strip().split(",")))
        file.readline()

        boards: list[Board] = []
        for board_str in file.read().strip().split("\n\n"):
            rows: list[list[Cell]] = []
            for row in board_str.split("\n"):
                rows.append(list(map(lambda n: Cell(value=int(n)), row.split())))
            boards.append(Board(rows))
    return nums, boards


def part1(filepath):
    nums, boards = read_inputs(filepath)
    for num in nums:
        for board in boards:
            board.mark_cells(num)
            if board.is_winning():
                return num * board.sum_unmarked()


def part2(filepath):
    nums, boards = read_inputs(filepath)
    winning_boards = set()

    for num in nums:
        for i, board in enumerate(boards):
            if i in winning_boards:
                continue
            board.mark_cells(num)
            if board.is_winning():
                winning_boards.add(i)
            if len(winning_boards) == len(boards):
                return num * board.sum_unmarked()


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
