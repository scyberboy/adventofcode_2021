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


def find_solution_a(data):
    data_len = len(data)
    most_common_treshould = data_len / 2
    bit_counter = Counter()
    gamma_rate_str = ""

    for row in data:
        row_dict = {idx: int(val) for idx, val in enumerate(row)}
        bit_counter.update(row_dict)

    print("bit_counter:", bit_counter.items())

    for val in bit_counter.values():
        gamma_rate_str += '1' if val > most_common_treshould else '0'

    print("gamma_rate_str:", gamma_rate_str)
    gamma_rate = int(gamma_rate_str, 2)
    epsilon_rate = gamma_rate ^ int("1" * (int.bit_length(gamma_rate)), 2)
    print("gamma_rate:\t{}({})".format(gamma_rate, bin(gamma_rate)))
    print("epsilon_rate:\t{}({})".format(epsilon_rate, bin(epsilon_rate)))

    answer = gamma_rate * epsilon_rate

    return answer


def find_solution_b(data):
    # sums_list = list(map(sum, zip(input_data, input_data[1:], input_data[2:])))
    # # print("sums_list", sums_list)
    # reduced_data_it = filter(bool, map(operator.lt, sums_list, sums_list[1:]))
    # reduced_data = list(reduced_data_it)
    # reduced_data_len = len(reduced_data)
    #
    # # print("reduced_data({}): {}".format(reduced_data_len, reduced_data))
    #
    # return reduced_data_len

    pass


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
