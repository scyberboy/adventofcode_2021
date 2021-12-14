import operator
import os
import re
import sys
import time

from collections import deque
from functools import reduce
import numpy as np


def read_input() -> list[list[int]]:
    # Read lines input:
    # 2199943210
    # 3987894921
    # 9856789892
    # 8767896789
    # 9899965678
    # return list with lists of integers [[r1.1,r1.2,r1.3...],[r2.1,r2.2,r2.3,...],...]
    # plus wrapped with max values (9) all around for easier low points search ;)

    data = [[int(elem) for elem in '9' + line.strip() + '9'] for line in sys.stdin]
    nr_additions = len(data[0])
    data.insert(0, [9 for _ in range(nr_additions)])
    data.append([9 for _ in range(nr_additions)])

    return data


def is_low_point(height_map: np.array, x_curr: int, y_curr: int) -> bool:
    val = height_map[x_curr, y_curr]
    hor_elems = [height_map[x_curr, y_curr - 1], height_map[x_curr, y_curr + 1]]
    ver_elems = [height_map[x_curr - 1, y_curr], height_map[x_curr + 1, y_curr]]

    all_elems = hor_elems + ver_elems
    min_elem = min(all_elems)
    if val < min_elem:
        return True

    return False


def find_low_points(height_map: np.array) -> list[(int, int), int]:
    candidates = list()
    # print("height map shape: {}".format(height_map.shape))
    x_dim, y_dim = height_map.shape
    for x_curr in range(1, x_dim - 1):
        for y_curr in range(1, y_dim - 1):
            if is_low_point(height_map, x_curr, y_curr):
                # print("low point found: [{}][{}] -> {}".format(x_curr, y_curr, height_map[x_curr, y_curr]))
                candidates.append([(x_curr, y_curr), height_map[x_curr, y_curr]])

    return candidates


def find_solution_a(low_points: list[(int, int), int]) -> int:
    answer = sum([elem[1] for elem in low_points]) + len(low_points)

    return answer


def generate_basin(height_map: np.array, x_y: (int, int)) -> list[(int, int)]:
    basin = set()
    candidates = deque()

    candidates.append(x_y)

    neigh_offsets = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    while len(candidates) > 0:

        # use DFS (depth first search) by simulating store in stack (FIFO)
        # x_curr, y_curr = candidates.pop()

        # use BFS (breadth first search) by simulating store in queue (FILO)
        x_curr, y_curr = candidates.popleft()

        # both methods should work

        basin.add((x_curr, y_curr))

        for x_off, y_off in neigh_offsets:
            candi_x = x_curr + x_off
            candi_y = y_curr + y_off

            cur_val = height_map[x_curr][y_curr]
            candi_val = height_map[candi_x][candi_y]

            if candi_val != 9 and candi_val > cur_val and\
                    (candi_x, candi_y) not in basin:
                candidates.append((candi_x, candi_y))

    return list(basin)


def find_solution_b(height_map: np.array, low_points: list[(int, int), int]) -> int:
    # print("low points: {}".format(low_points))
    basin_sizes = list()
    for x_y, _ in low_points:
        basin = generate_basin(height_map, x_y)
        if len(basin) > 0:
            basin_sizes.append(len(basin))

    answer = reduce(operator.mul, sorted(basin_sizes, reverse=True)[:3], 1)

    return answer


def do_main():

    prev_time = time.process_time()

    print("start reading input...")
    data = read_input()
    cur_time = time.process_time()
    diff = cur_time - prev_time
    prev_time = cur_time
    print("[{}] took: {} sec.".format(cur_time, diff))

    # print("input data: {}".format(data))

    print("generate low points...")
    height_map = np.array(data)
    low_points = find_low_points(height_map)
    cur_time = time.process_time()
    diff = cur_time - prev_time
    prev_time = cur_time
    print("[{}] took: {} sec.".format(cur_time, diff))

    print("find_solution_a...")
    result_a = find_solution_a(low_points)
    print("result_a:", result_a)
    cur_time = time.process_time()
    diff = cur_time - prev_time
    prev_time = cur_time
    print("[{}] took: {} sec.".format(cur_time, diff))

    print("find_solution_b...")
    result_b = find_solution_b(height_map, low_points)
    print("result_b:", result_b)
    cur_time = time.process_time()
    diff = cur_time - prev_time
    # prev_time = cur_time
    print("[{}] took: {} sec.".format(cur_time, diff))



if __name__ == "__main__":
    # execute only if run as a script

    filename = os.path.basename(__file__)
    day_nr = re.search(r"\d+", filename).group()
    print("day_nr:", day_nr)

    do_main()
