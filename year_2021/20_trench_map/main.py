# https://adventofcode.com/2021/day/20

# Type aliases
Image = list[list[str]]

Pos = tuple[int, int]


def read_inputs(filepath) -> tuple[str, Image]:
    with open(filepath) as file:
        algorithm, trench_map = file.read().strip().split("\n\n")
        return algorithm, [list(row) for row in trench_map.splitlines()]


def square_neighborhood(x: int, y: int) -> list[Pos]:
    return [(x + dx, y + dy) for dx in range(-1, 2) for dy in range(-1, 2)]


def new_value(algorithm: str, key: str) -> str:
    return algorithm[int(key.replace(".", "0").replace("#", "1"), base=2)]


def grow(image: Image, infinite_pixel: str, expand=3) -> Image:
    nrows, ncols = len(image), len(image[0])
    new_image = [
        [infinite_pixel] * (ncols + expand * 2) for _ in range(nrows + expand * 2)
    ]
    for r in range(nrows):
        for c in range(ncols):
            new_image[r + expand][c + expand] = image[r][c]
    return new_image


def enhance(algorithm: str, image: Image, infinite_pixel: str) -> tuple[Image, str]:
    nrows, ncols = len(image), len(image[0])
    new_infinite_pixel = new_value(algorithm, infinite_pixel * 9)
    new_image = [[new_infinite_pixel] * ncols for _ in range(nrows)]

    for r in range(nrows):
        for c in range(ncols):
            key = "".join(
                image[nr][nc] if 0 <= nr < nrows and 0 <= nc < ncols else infinite_pixel
                for nr, nc in square_neighborhood(r, c)
            )
            new_image[r][c] = new_value(algorithm, key)
    return new_image, new_infinite_pixel


def count_lits(
    algorithm: str, image: Image, infinite_pixel=".", nb_enhancement=2
) -> int:
    for i in range(nb_enhancement):
        # Try to grow only if necessary
        # In practice we don't gain much but it's fine
        if i % 3 == 0:
            image = grow(image, infinite_pixel, expand=4)
        image, infinite_pixel = enhance(algorithm, image, infinite_pixel)
    return sum(row.count("#") for row in image)


def part1(filepath):
    algorithm, image = read_inputs(filepath)
    return count_lits(algorithm, image)


def part2(filepath):
    algorithm, image = read_inputs(filepath)
    return count_lits(algorithm, image, nb_enhancement=50)


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
