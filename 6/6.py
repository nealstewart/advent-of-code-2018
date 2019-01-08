import matplotlib.pyplot as plt
from typing import List, Tuple
import numpy as np

Spot = Tuple[int, int]

def get_tuple(line: str):
    a, b = [int(part.strip()) for part in line.split(",")]
    return (a, b)

def get_input() -> List[Spot]:
    with open('input') as f:
        return [get_tuple(line) for line in f]

def get_bounds(spots: List[Spot]):
    x = max(spots, key=lambda s: s[0])[0]
    y = max(spots, key=lambda s: s[1])[1]
    return (x, y)

def calc_distance(a: Spot, b: Spot) -> int:
    ax, ay = a
    bx, by = b
    return abs(ax - bx) + abs(ay - by)

def find_closest_index(spots: List[Spot], spot: Spot) -> int:
    closest = (-1, np.Infinity)

    for ix, other_spot in enumerate(spots):
        distance = calc_distance(other_spot, spot)

        if distance == 0:
            return ix

        if distance < closest[1]:
            closest = (ix, distance)
        elif distance == closest[1]:
            closest = (-1, distance)

    return closest[0]


def render_solution_space(spots: List[Spot], space: np.ndarray, step: int):
    plt.imshow(space.T, cmap='hot', interpolation='nearest')
    plt.savefig(f'heatmap{step}.png')
    plt.scatter([spot[0] for spot in spots], [spot[1] for spot in spots])
    for ix, spot in enumerate(spots):
        plt.text(spot[0], spot[1], str(ix))
    plt.savefig(f'spots{step}.png')

def is_infinite_section(mask: np.ndarray):
    # If any section along an edge in the boolean mask is closest to this index
    # then the section is likely infinite.
    edges = [
        mask[0, :],
        mask[:, 0],
        mask[-1, :],
        mask[:, -1]
    ]

    return any(np.any(edge) for edge in edges)

def solve_part_1():
    spots = get_input()
    bounds = get_bounds(spots)
    solution = np.ndarray(shape=bounds, dtype=np.int32)

    for x in range(0, solution.shape[0]):
        for y in range(0, solution.shape[1]):
            solution[x, y] = find_closest_index(spots, (x, y))

    render_solution_space(spots, solution, 1)

    def get_sum(ix: int):
        mask = solution == ix

        if is_infinite_section(mask):
            return 0

        return np.sum(mask)

    largest_area = max([get_sum(ix) for ix in range(0, len(spots))])
    print("Solution for part 1", largest_area)

def solve_part_2():
    spots = get_input()
    bounds = get_bounds(spots)
    solution_space = np.ndarray(shape=bounds, dtype=np.int32)
    for x in range(0, solution_space.shape[0]):
        for y in range(0, solution_space.shape[1]):
            solution_space[x, y] = sum([calc_distance((x, y), spot) for spot in spots])

    render_solution_space(spots, solution_space, 2)

    print("Solution for part 2", np.sum(solution_space < 10000))

solve_part_1()
solve_part_2()