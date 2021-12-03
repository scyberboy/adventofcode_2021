import operator
import sys
import os
import re


def read_input():
    for line in sys.stdin:
        input_data.append(line.strip())


def find_solution_a():
    reduced_data_it = filter(bool, map(operator.lt, input_data, input_data[1:]))
    reduced_data = list(reduced_data_it)
    reduced_data_len = len(reduced_data)

    # print("reduced_data({}): {}".format(reduced_data_len, reduced_data))

    return reduced_data_len


def find_solution_b():
    sums_list = list(map(sum, zip(input_data, input_data[1:], input_data[2:])))
    # print("sums_list", sums_list)
    reduced_data_it = filter(bool, map(operator.lt, sums_list, sums_list[1:]))
    reduced_data = list(reduced_data_it)
    reduced_data_len = len(reduced_data)

    # print("reduced_data({}): {}".format(reduced_data_len, reduced_data))

    return reduced_data_len


def do_main():

    read_input()
    # print("input_data", input_data)

    result_a = find_solution_a()
    print("result_a:", result_a)

    result_b = find_solution_b()
    print("result_b:", result_b)


if __name__ == "__main__":
    # execute only if run as a script

    filename = os.path.basename(__file__)
    day_nr = re.search(r"\d+", filename).group()
    print("day_nr:", day_nr)

    do_main()
