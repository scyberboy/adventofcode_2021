import os
import re
import sys
import time


def read_input() -> tuple[list[list[str]], list[list[str]]]:
    """

    """
    # Read lines input:
    # be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
    # edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc

    # keep the dot's as list of two elements tuple (int, int) - (0, 5)
    wire_signals = list()
    # instructions as list of two elements (int, int) - (0, 7), where first is (0->x or 1->y), second is the axis
    segment_signals = list()

    while True:
        line = sys.stdin.readline()
        if line == "\n" or line == "":
            break
        group = line.strip().split(" | ")
        wire_signals.append([code for code in group[0].split(" ")])
        segment_signals.append([code for code in group[1].split(" ")])

    # return two lists:
    return wire_signals, segment_signals


def find_solution_a(segment_signals: list[list[str]]) -> int:
    # count the 2, 3, 4 and 7 length strings which corresponds
    # to number 1, 7, 4 and 8
    cnt = 0
    for code in [code for line in segment_signals for code in line]:
        cnt += 1 if len(code) in [2, 3, 4, 7] else 0

    return cnt


def find_solution_b():
    pass


def do_main():
    prev_time = time.process_time()

    print("start reading input...")
    wire_signals, segment_signals = read_input()
    cur_time = time.process_time()
    diff = cur_time - prev_time
    prev_time = cur_time
    print("[{}] took: {} sec.".format(cur_time, diff))

    # print("wire_signals: {}".format(wire_signals))
    # print("segment_signals: {}".format(segment_signals))

    print("find_solution_a...")
    result_a = find_solution_a(segment_signals)
    print("result_a:", result_a)
    cur_time = time.process_time()
    diff = cur_time - prev_time
    prev_time = cur_time
    print("[{}] took: {} sec.".format(cur_time, diff))

    print("find_solution_b...")
    result_b = find_solution_b()
    print("result_b:", result_b)
    cur_time = time.process_time()
    diff = cur_time - prev_time
    print("[{}] took: {} sec.".format(cur_time, diff))


if __name__ == "__main__":
    # execute only if run as a script

    filename = os.path.basename(__file__)
    day_nr = re.search(r"\d+", filename).group()
    print("day_nr:", day_nr)

    do_main()
