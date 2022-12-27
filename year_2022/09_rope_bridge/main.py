from dataclasses import dataclass, astuple


@dataclass
class Motion:
    direction: str
    distance: int


def read_inputs(filename):
    with open(filename) as file:
        for line in file.readlines():
            direction, distance = line.strip().split()
            distance = int(distance)
            yield Motion(direction, distance)


@dataclass
class Point:
    x: int = 0
    y: int = 0

    def distance(self, other) -> int:
        return max(abs(self.x - other.x), abs(self.y - other.y))

    def is_close(self, other) -> bool:
        return self.distance(other) <= 1

    def __hash__(self) -> int:
        return hash(astuple(self))


class Rope:
    def __init__(self, length: int) -> None:
        self.knots = [Point(x=0, y=0) for _ in range(length)]
        self._visited = set()
        self._update_visited()
        self._length = length

    @property
    def count_visited(self) -> int:
        return len(self._visited)

    def move_head(self, direction: str) -> None:
        head = self.knots[0]
        if direction == "R":
            head.x += 1
        if direction == "L":
            head.x -= 1
        if direction == "U":
            head.y += 1
        if direction == "D":
            head.y -= 1

    def move_body(self, i: int) -> None:
        if i < 1:
            raise ValueError("knot in body should have index >= 1")
        head = self.knots[i - 1]
        tail = self.knots[i]

        if tail.is_close(head):
            return

        incx = 1 if tail.x < head.x else -1
        incy = 1 if tail.y < head.y else -1

        if tail.y == head.y:
            # Move the tail along x-axis
            tail.x += incx
        elif tail.x == head.x:
            # Move the tail along y-axis
            tail.y += incy
        else:
            # Move diagonally
            tail.x += incx
            tail.y += incy

    def move(self, motion: Motion) -> None:
        for _ in range(motion.distance):
            self.move_head(motion.direction)
            for i in range(1, self._length):
                self.move_body(i)
                # Mark tail as seen
                self._update_visited()

    def _update_visited(self):
        self._visited.add(astuple(self.knots[-1]))

    def __getitem__(self, i: int) -> Point:
        return self.knots[i]


def simulate_motion(filename, nb_knots=2):
    rope = Rope(nb_knots)
    for motion in read_inputs(filename):
        rope.move(motion)
    return rope.count_visited


def main(filename):
    print("Part 1:", simulate_motion(filename, nb_knots=2))
    print("Part 2:", simulate_motion(filename, nb_knots=10))
