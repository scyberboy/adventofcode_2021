import operator
import sys
import os
import re

# day 3 input is sequence of binary data:
# 101101101001
# 100001100100
# 000111010100
# most common bit for each position is the gamma rate
# least common bit for each position is the epsilon rate
# so, one is the complement of other (and vice versa)
from collections import Counter


def read_input():
    data = [line.strip() for line in sys.stdin]
    return data


def __generate_inverse_uint(value):
    # type: (int) -> int
    inversed = value ^ int("1" * (int.bit_length(value)), 2)

    return inversed


def __generate_counter(data):
    # type (list) -> collections.Counter
    bit_counter = Counter()

    for row in data:
        row_dict = {idx: int(val) for idx, val in enumerate(row)}
        bit_counter.update(row_dict)

    return bit_counter


def find_solution_a(data):
    data_len = len(data)
    most_common_treshould = data_len / 2
    gamma_rate_str = ""

    bit_counter = __generate_counter(data)
    # print("bit_counter:", bit_counter.items())

    for val in bit_counter.values():
        gamma_rate_str += '1' if val > most_common_treshould else '0'

    # print("gamma_rate_str:", gamma_rate_str)
    gamma_rate = int(gamma_rate_str, 2)
    epsilon_rate = __generate_inverse_uint(gamma_rate)
    # print("gamma_rate:\t{}({})".format(gamma_rate, bin(gamma_rate)))
    # print("epsilon_rate:\t{}({})".format(epsilon_rate, bin(epsilon_rate)))

    answer = gamma_rate * epsilon_rate

    return answer


def __filter_data(data, bit_index, crit, value):
    # type (list, int, Union[operator.le, operator.ge], Union[str, int]) -> list
    """
    Filter until only one record remains (recursively). Then return it.
    The filtering is done based on the most/ the least common bit for the given position.

    :param data: List of strings (representing binary numbers, i.e. 1001101)
    :param bit_index: Index of the bit we're filtering on atm
    :param crit: Criterion (>= or <=) in order to fine most/least common bit
    :param value: Leading value to use (0 or 1)
    :return: List (the filtered data)
    """
    data_len = len(data)
    half_data_len = len(data) / 2

    # print("\tdata len: {}, bit_index: {}, criterion: {}, value: {}".format(data_len, bit_index, crit, value))
    # if data_len < 15:
    #     print("\tdata:", data)

    if data_len == 1:
        return data[0]

    # another guard statement (should not happen ever if the input data is correct)
    if len(data) == 0 or bit_index >= len(data[0]):
        raise NotImplementedError("Something weird happened - entry length is exhausted, but no solution is found!")

    data_counter = __generate_counter(data)
    # print("\tdata_counter:", data_counter.items())

    if data_counter[bit_index] > half_data_len:
        prevailing_val = 1
    else:
        prevailing_val = 0

    # print("\tprevailing_val:", prevailing_val)

    # the key comparison...
    if data_counter[bit_index] == half_data_len:
        interesting_val = value  # default given
    elif crit(0.5, 1):  # least
        interesting_val = 1 - prevailing_val
    # least (<) (lt) 0
    else:  # most
        interesting_val = prevailing_val

    # print("\tinteresting_val:", interesting_val)

    new_data = [elem for elem in data if elem[bit_index] == str(interesting_val)]
    return __filter_data(new_data, bit_index+1, crit, value)


def find_solution_b(data):
    data_len = len(data)

    # print("find oxy_gen_str...")
    oxy_gen_str = __filter_data(data, 0, operator.gt, 1)
    # print("oxy_gen_str:", oxy_gen_str)
    # print("find carbond_scrub_str...")
    carbond_scrub_str = __filter_data(data, 0, operator.lt, 0)
    # print("carbond_scrub_str:", carbond_scrub_str)

    oxy_gen = int(oxy_gen_str, 2)
    carbond_scrub = int(carbond_scrub_str, 2)

    answer = oxy_gen * carbond_scrub
    # print("life support rating: {} <- oxy_gen: {}, carbond_scrub: {}".format(answer, oxy_gen, carbond_scrub))

    return answer


def do_main():

    input_data = read_input()
    # print("input_data", input_data)

    result_a = find_solution_a(input_data)
    print("result_a:", result_a)

    result_b = find_solution_b(input_data)
    print("result_b:", result_b)


if __name__ == "__main__":
    # execute only if run as a script

    filename = os.path.basename(__file__)
    day_nr = re.search(r"\d+", filename).group()
    print("day_nr:", day_nr)

    do_main()
