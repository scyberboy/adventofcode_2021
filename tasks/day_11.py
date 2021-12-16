import os
import re
import sys
import time


def read_input() -> list[int]:
    """

    :return:
    """
    # Read lines input:
    # [({(<(())[]>[[{[]{<()<>>
    # [(()[<>])]({[<{<<[]>>(
    # {([(<{}[<>[]}>{[]{[(<()>
    # (((({<>}<{<{<>}{[]{[]{}

    return [int(elem) for elem in sys.stdin.read() if elem != "\n"]


def increase_neigh_levels(octos: list[int], idx_maxer: int) -> None:
    row_idx = idx_maxer % 10
    # [-11, -10, -9, -1, 1, 9, 10, 11]
    if row_idx == 0:
        # beginning
        neigh_offsets = [-10, -9, 1, 10, 11]
    elif row_idx == 9:
        # end
        neigh_offsets = [-11, -10, -1, 9, 10]
    else:
        # middle (all)
        neigh_offsets = [-11, -10, -9, -1, 1, 9, 10, 11]

    for offset in neigh_offsets:
        target_idx = idx_maxer + offset

        # skip overall invalid indexes
        if target_idx < 0 or target_idx >= len(octos):
            continue

        # the rest should be all valid, if it hasn't flashed already - increase it
        if octos[target_idx] > 0:
            octos[target_idx] += 1


def find_solution(octos: list[int], nr_steps: int) -> int:
    total_flashes = 0
    for step in range(nr_steps):

        # 1. increase all octos energy level
        for idx in range(len(octos)):
            octos[idx] += 1

        # 2. process until no flashers left
        while max(octos) > 9:
            maxer = max(octos)
            idx_maxer = octos.index(maxer)

            # 2.1 flash it - set to 0 and increase neigh energy level
            octos[idx_maxer] = 0
            total_flashes += 1
            increase_neigh_levels(octos, idx_maxer)

        # solution (b)
        if max(octos) == 0:
            return step + 1

    return total_flashes


def do_main():
    prev_time = time.process_time()

    print("start reading input...")
    data = read_input()
    cur_time = time.process_time()
    diff = cur_time - prev_time
    prev_time = cur_time
    print("[{}] took: {} sec.".format(cur_time, diff))

    # print("input data: {}".format(data))

    print("find_solution_a...")
    result_a = find_solution(data.copy(), 100)
    print("result_a:", result_a)
    cur_time = time.process_time()
    diff = cur_time - prev_time
    prev_time = cur_time
    print("[{}] took: {} sec.".format(cur_time, diff))

    print("find_solution_b...")
    result_b = find_solution(data.copy(), sys.maxsize)
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
