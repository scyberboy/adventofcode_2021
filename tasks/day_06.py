import collections
import os
import re
import sys


lower_limit = 0
upper_limit = 6
newborn_handicap = 2


def read_input():
    # Read lines input, ribki -> 4,3,2,1,5,6,3....
    # return list with integers

    data = [int(elem) for elem in sys.stdin.readline().split(",")]

    return data


def find_solution_b(data, nr_days):
    # type:(list, int) -> int
    """
    Poneje dnite sa mnogo nad 80 (256), tva ne moje da se smetne s brute force.
    Trqa izmislim neshto umno :)

    :param data:
    :param nr_days:
    :return:
    """
    initial_cntr = collections.Counter(data)
    # print("life period: {} \n initial cntr: {}".format(nr_days, sorted(initial_cntr.items())))

    for _day in range(nr_days):

        new_cntr = collections.Counter()
        for _key, _val in initial_cntr.items():
            new_timer = _key - 1
            if new_timer < 0:
                new_cntr[upper_limit] += _val
                new_cntr[upper_limit + newborn_handicap] += _val
            else:
                new_cntr[new_timer] += _val

        # at the end of the day set the main counter
        # print("new cntr {:3d}: {}".format(_day, sorted(new_cntr.items())))
        if len(new_cntr) > 0:
            initial_cntr = new_cntr

    # print("final cntr: {}".format(sorted(initial_cntr.items())))

    return sum(initial_cntr.values())


def find_solution_a(data, nr_days):
    # type:(list, int) -> int

    # get safe copy (don't alter the outside collection)
    initial_data = data.copy()
    # print("life period: {}, initial data: {}".format(nr_days, data))

    for _day in range(nr_days):

        # print("data({}): {}".format(_day, data))

        malki_ribki = list()
        for idx, ribka_clock in enumerate(initial_data):
            new_val = ribka_clock - 1
            if new_val < lower_limit:
                initial_data[idx] = upper_limit
                malki_ribki.append(upper_limit + newborn_handicap)
            else:
                initial_data[idx] = new_val

        # at the end of the day add all spawned newborns to cycle (if any)
        if len(malki_ribki) > 0:
            initial_data = initial_data + malki_ribki

    return len(initial_data)


def do_main():

    ribki = read_input()

    # use the smart solution for both parts :)

    # NB: solution_a do manipulate the initial data, and it gets changed, so hampered initial for solution_b
    #   I thought the frothing Python can't do this (modify function parameters, like by reference in C/C++)
    #   DFQ :)

    result_a = find_solution_b(ribki, 80)
    print("result_a:", result_a)

    result_b = find_solution_b(ribki, 256)
    print("result_b:", result_b)


if __name__ == "__main__":
    # execute only if run as a script

    filename = os.path.basename(__file__)
    day_nr = re.search(r"\d+", filename).group()
    print("day_nr:", day_nr)

    do_main()
