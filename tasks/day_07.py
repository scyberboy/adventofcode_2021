from collections import Counter
import os
import re
import sys


def read_input():
    # Read lines input, raci -> 4,3,2,1,5,6,3....
    # return list with integers

    data = [int(elem) for elem in sys.stdin.readline().split(",")]

    return data


def calc_cost_to_target(raci_to_move, target, consumption="linear"):
    # type:(dict, int, str) -> int
    """

    :param consumption: type of fuel consumption Union[linear,any]
    :param raci_to_move:
    :param target:
    :return: the cost to move all elements from raci_to_move to target
    """

    total_cost = 0
    for source, qty in raci_to_move.items():
        dist = abs(source - target)
        if consumption == "linear":
            total_cost += (dist * qty)
        else:  # it's algebraic progression
            total_cost += (sum(range(1, dist+1)) * qty)

    return total_cost


def find_solution_a(data, type_of_consumption="linear"):
    # type:(list, str) -> int

    # get safe copy (don't alter the outside collection)

    initial_cntr = Counter(data)
    # print("initial counter: {}".format(initial_cntr))
    most_common_dict = {k: v for (k, v) in initial_cntr.most_common()}
    # print("most_common_dict: {}".format(most_common_dict))

    # as the possible solution target(points) may be in between the raci
    # prepare a series of ones from min(rak_coords) to max(rak_coords)
    min_coord = min(most_common_dict.keys())
    max_coord = max(most_common_dict.keys())

    # start calculating the costs from the most common point consecutively
    # candidate doesn't count as we are aiming at it
    cost_to_target = dict()
    for coord in range(min_coord, max_coord+1):
        cost_to_target[coord] = calc_cost_to_target(most_common_dict, coord, type_of_consumption)
        # print("cost_to_target: {}".format(cost_to_target))

    result_cntr = Counter(cost_to_target)
    answer = result_cntr.most_common()
    # print("all possible vals sorted, {} consumption: {}". format(type_of_consumption, answer))

    # take the last one (the rarest == cheapest)
    (_, val) = answer[-1]

    return val


def do_main():

    raci = read_input()

    # use the smart solution for both parts :)

    result_a = find_solution_a(raci)
    print("result_a:", result_a)

    result_b = find_solution_a(raci, type_of_consumption="algebraic")
    print("result_b:", result_b)


if __name__ == "__main__":
    # execute only if run as a script

    filename = os.path.basename(__file__)
    day_nr = re.search(r"\d+", filename).group()
    print("day_nr:", day_nr)

    do_main()
