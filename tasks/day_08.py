import os
import re
import sys


def read_input():
    # Read lines input, raci -> 4,3,2,1,5,6,3....
    # return list with integers

    data = [int(elem) for elem in sys.stdin.readline().split(",")]

    return data


def find_solution_a():
    pass


def find_solution_b():
    pass


def do_main():

    raci = read_input()

    # use the smart solution for both parts :)

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
