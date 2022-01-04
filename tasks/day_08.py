import os
import re
import sys
import time
from itertools import permutations


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


def calc_diff(base_list: list[str], sub_list: list[str]) -> list[str]:
    res_list = list()

    # if the sub_list is present in base_list permutations discard
    # otherwise keep - it's diff
    perm_len = len(sub_list[0])
    sub_list_base_elem = "".join(sorted(sub_list[0]))

    for base_elem in base_list:
        perms_list = (["".join(elem) for elem in permutations(base_elem, perm_len)])
        if sub_list_base_elem not in perms_list:
            res_list.append(base_elem)

    return res_list


def process_line_codes(wire_signals: list[str], segment_signals: list[str]) -> int:
    #    8:
    #   aaaa
    #  b    c
    #  b    c
    #   dddd
    #  e    f
    #  e    f
    #   gggg

    # number -> len
    # 0 -> 6
    # 1 -> 2 UNIQ
    # 2 -> 5
    # 3 -> 5
    # 4 -> 4 UNIQ
    # 5 -> 5
    # 6 -> 6
    # 7 -> 3 UNIQ
    # 8 -> 7 UNIQ
    # 9 -> 6

    # len -> numbers list
    # 2 -> [1]
    # 3 -> [7]
    # 4 -> [4]
    # 5 -> [2,3,5]
    # 6 -> [0,6,9]
    # 7 -> [8]

    ones_codes = list()
    sevens_codes = list()
    fours_codes = list()
    eights_codes = list()
    twos_threes_fives_codes = list()
    zeros_sixes_nines_codes = list()

    for code in [dumb for dumb in wire_signals if len(dumb) == 2]:
        # print("1")
        # ones_codes.extend(["".join(elem) for elem in permutations(code, len(code))])
        ones_codes.append(code)

    for code in [dumb for dumb in wire_signals if len(dumb) == 3]:
        # print("2")
        # sevens_codes.extend(["".join(elem) for elem in permutations(code, len(code))])
        sevens_codes.append(code)

    for code in [dumb for dumb in wire_signals if len(dumb) == 4]:
        # print("3")
        # fours_codes.extend(["".join(elem) for elem in permutations(code, len(code))])
        fours_codes.append(code)

    for code in [dumb for dumb in wire_signals if len(dumb) == 7]:
        # print("4")
        # eights_codes.extend(["".join(elem) for elem in permutations(code, len(code))])
        # PERFORMANCE IMPROVEMENT - reduce usage of permutations!!!
        eights_codes.append(code)

    for code in [dumb for dumb in wire_signals if len(dumb) == 5]:
        # print("5")
        # twos_threes_fives_codes.extend(["".join(elem) for elem in permutations(code, len(code))])
        twos_threes_fives_codes.append(code)

    for code in [dumb for dumb in wire_signals if len(dumb) == 6]:
        # print("6")
        # zeros_sixes_nines_codes.extend(["".join(elem) for elem in permutations(code, len(code))])
        zeros_sixes_nines_codes.append(code)

    # print("ones_codes({}): {}".format(len(ones_codes), ones_codes))
    # print("sevens_codes({}): {}".format(len(sevens_codes), sevens_codes))
    # print("fours_codes({}): {}".format(len(fours_codes), fours_codes))
    # print("eights_codes({}): {}".format(len(eights_codes), eights_codes))
    # print("twos_threes_fives_codes({}): {}".format(len(twos_threes_fives_codes), twos_threes_fives_codes))
    # print("zeros_sixes_nines_codes({}): {}".format(len(zeros_sixes_nines_codes), zeros_sixes_nines_codes))

    # 1 !!!
    # 4 !!!
    # 7 !!!
    # 8 !!!

    # 0, 6, 9 - 7 => 6 !!!
    # 0, 6, 9 - 4 => 0, 6 !
    # 0, 6, 9 - 0, 6 => 9 !!!
    # 0, 6, 9 - 6 - 9 => 0 !!!

    # 8 - 6 => us1 !
    # 1 - us1 => ls1 !

    # 2, 3, 5 - us1 => 5 !!!
    # 2, 3, 5 - ls1 => 2 !!!
    # 2, 3, 5 - 5 - 2 => 3 !!!

    codes_by_digit = dict()

    # ones, fours, sevens, eights
    codes_by_digit[1] = ones_codes
    codes_by_digit[7] = sevens_codes
    codes_by_digit[4] = fours_codes
    codes_by_digit[8] = eights_codes

    # sixes
    codes_by_digit[6] = calc_diff(zeros_sixes_nines_codes, sevens_codes)

    # zeros
    zero_six_codes = calc_diff(zeros_sixes_nines_codes, fours_codes)
    codes_by_digit[0] = calc_diff(zero_six_codes, codes_by_digit[6])

    # nines
    codes_by_digit[9] = calc_diff(calc_diff(zeros_sixes_nines_codes, codes_by_digit[0]), codes_by_digit[6])

    # intermediates:
    # us1 (upper segment of 1)
    # ls1 (loser segment of 1)

    us1 = list(set(sorted(codes_by_digit[8][0])) - set(sorted(codes_by_digit[6][0])))
    ls1 = list(set(sorted(codes_by_digit[1][0])) - set(sorted(us1)))

    # print("us1: {}".format(us1))
    # print("ls1: {}".format(ls1))

    if len(us1) > 1 or len(ls1) > 1:
        raise ValueError("SHIT")

    # fives
    tmp_lst = calc_diff(twos_threes_fives_codes, us1)
    codes_by_digit[5] = tmp_lst

    # twos
    tmp_lst = calc_diff(twos_threes_fives_codes, ls1)
    codes_by_digit[2] = tmp_lst

    # threes
    tmp_lst = calc_diff(twos_threes_fives_codes, codes_by_digit[5])
    tmp_lst = calc_diff(tmp_lst, codes_by_digit[2])
    codes_by_digit[3] = tmp_lst

    # for key in codes_by_digit:
    #     print("codes_by_digit({})[{}]: {}".format(len(codes_by_digit[key]), key, codes_by_digit[key]))

    # NOW - I have all digits codes for current line
    number_str = ""
    for segment in segment_signals:
        for idx, code in codes_by_digit.items():
            code_perms = ["".join(elem) for elem in permutations(code[0], len(code[0]))]
            # print("segment: {}, idx: {}, code(s): {} -> perms: {}".format(segment, idx, code, code_perms))
            if segment in code_perms:
                # print("segment: {} -> {}".format(segment, idx))
                number_str += str(idx)
                break

    line_code_number = int(number_str)

    return line_code_number


def find_solution_b(wire_signals: list[list[str]], segment_signals: list[list[str]]) -> int:

    sum_line_codes = 0
    for wire_sig, segm_sig in zip(wire_signals, segment_signals):
        # print("PROCESSING {} | {}".format(wire_sig, segm_sig))
        line_code = process_line_codes(wire_sig, segm_sig)
        # print("FOUND CODE -> {}".format(line_code))
        sum_line_codes += line_code

    return sum_line_codes


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
    result_b = find_solution_b(wire_signals, segment_signals)
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
