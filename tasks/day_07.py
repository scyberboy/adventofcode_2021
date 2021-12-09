import time
from collections import Counter
import numpy as np
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

    # note: sbora na S:E e
    # 			<sbora na granicite> po <polovinata ot broq>
    # chetni: 	SUM = (S + E) * (E - S) / 2
    # nechetni: 	<sbora na granicite> po <polovinata ot broq> + <srednoto chislo ot intervala)
    # 			SUM = (S + E) * (E - S) / 2 + ((E - S) / 2 + 1)

    total_cost = 0
    for source, qty in raci_to_move.items():
        dist = abs(source - target)
        if consumption == "linear":  # it's linear progression
            total_cost += (dist * qty)
        else:  # it's arithmetic progression
            # Move from 16 to 5: 66 fuel
            # Move from 1 to 5: 10 fuel
            # Move from 2 to 5: 6 fuel
            if dist % 2 == 0:  # chetni
                adder = (1 + dist) * dist // 2
            else:  # nechetni
                adder = (1 + dist) * (dist // 2) + (dist // 2 + 1)
            total_cost += (int(adder) * qty)

    return total_cost


def find_solution_a(data, type_of_consumption="linear"):
    # type:(list, str) -> int

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
    print("last 10 MCV, {} consumption: {}". format(type_of_consumption, answer[-10:]))

    # take the last one (the rarest == cheapest)
    (_, val) = answer[-1]

    return val


def generate_candidates_list(starting_coord, min_coord, max_coord):
    # type:(int, int, int) -> list
    result = list()
    result.append(int(starting_coord))
    # we'll generate thus many pairs growing +1/-1 from starting coord
    limit = min(abs(starting_coord-min_coord), abs(starting_coord-max_coord))
    for adder in range(1, int(limit)):
        result.append(int(starting_coord) + adder)
        result.append(int(starting_coord) - adder)

    return result


def find_solution_b(data, type_of_consumption="linear"):
    # type:(list, str) -> int

    # Won't use brute force, but will choose the candidates 1 by 1
    # Starting from the average or median of whole input values (the crab's coordinates)
    # for linear consumption - median (indeed, it's almost sure this is the exact point we need)
    # for arithmetic progressive consumption - average, then go both directions by +1/-1
    # After 10 operations observe the result and if it's 'сходим', t.e. constantly increasing
    # stop and take the first (smallest) calculated value.

    most_common_dict = {k: v for (k, v) in Counter(data).most_common()}
    min_coord = min(data)
    max_coord = max(data)
    starting_coord = np.median(data) if type_of_consumption == "linear" else np.average(data)

    # start calculating the costs from the most common point consecutively
    cost_to_target = dict()
    current_winner = float("inf")
    for coord in generate_candidates_list(starting_coord, min_coord, max_coord):
        cost_to_target[coord] = calc_cost_to_target(most_common_dict, coord, type_of_consumption)
        # print("cost_to_target: {}".format(cost_to_target))

        # update the current winner if such have just been found
        if cost_to_target[coord] < current_winner:
            current_winner = cost_to_target[coord]

        # check every X iterations, if the winner is the same. If it is - stop (use it)

        # NB: this optimization is kind if irrelevant (non-significant)
        #   so, rather skip it for the current set of data

        # if len(cost_to_target) % 1000 == 0:
        #     tmp_cntr = Counter(cost_to_target)
        #     tmp_answer = tmp_cntr.most_common()
        #     # print("\ttmp_answer[-10:]: {}".format(tmp_answer[-10:]))
        #     (_, tmp_val) = tmp_answer[-1]
        #
        #     if tmp_val == current_winner:
        #         break

    result_cntr = Counter(cost_to_target)
    answer = result_cntr.most_common()
    print("last 10 MCV, {} consumption: {}".format(type_of_consumption, answer[-10:]))

    # take the last one (the rarest == cheapest)
    (_, val) = answer[-1]

    return val


def do_main():

    raci = read_input()

    # use the smart solution for both parts :)

    print("--------")
    result_a = find_solution_a(raci, type_of_consumption="linear")
    print("result_a(brute):", result_a)
    print("Total elapsed: {} sec.".format(time.process_time()))

    print("--------")
    result_b = find_solution_a(raci, type_of_consumption="arithmetic")
    print("result_b(brute):", result_b)
    print("Total elapsed: {} sec.".format(time.process_time()))

    print("--------")
    result_a = find_solution_b(raci, type_of_consumption="linear")
    print("result_a(smart):", result_a)
    print("Total elapsed: {} sec.".format(time.process_time()))

    print("--------")
    result_b = find_solution_b(raci, type_of_consumption="arithmetic")
    print("result_b(smart):", result_b)
    print("Total elapsed: {} sec.".format(time.process_time()))


if __name__ == "__main__":
    # execute only if run as a script

    filename = os.path.basename(__file__)
    day_nr = re.search(r"\d+", filename).group()
    print("day_nr:", day_nr)

    do_main()
