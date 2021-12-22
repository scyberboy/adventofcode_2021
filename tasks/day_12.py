import collections
import copy
import os
import pprint
import re
import sys
import time


def read_input() -> list[str]:
    """

    :return:
    """
    # Read lines input:
    # dc-end
    # HN-start
    # start-kj
    # dc-start
    # dc-HN

    return [line.strip() for line in sys.stdin]


def is_target_node_eligible(curr_path: list[str], target_node: str) -> bool:
    node_counter = collections.Counter(curr_path)

    if target_node not in curr_path:
        return True

    for val, cntr in node_counter.items():
        if val.islower() and cntr > 1:
            return False

    return True


def generate_paths_to_end(inner_graph: dict[str:list[str]], all_paths: list[list[str]], curr_path: list[str],
                          curr_node: str, lvl=0) -> None:

    # print("[{}] curr_node: {} -> inner_graph: {}".format(lvl, curr_node, pprint.pformat(inner_graph)))

    curr_path.append(curr_node)
    # print("[{}] curr_path: {}".format(lvl, pprint.pformat(curr_path)))

    if curr_node == "end":
        # save the current path so far in the all paths list
        all_paths.append(curr_path)
        # print("[{}] just saved curr_path: {}".format(lvl, curr_path))
        # print("[{}] all_paths become: {}".format(lvl, all_paths))
        return

    for target_node in sorted(inner_graph[curr_node]):

        new_graph = copy.deepcopy(inner_graph)

        is_eligible = is_target_node_eligible(curr_path, target_node)

        if target_node.islower() and not is_eligible:
            new_graph[curr_node].remove(target_node)
            if len(new_graph[curr_node]) == 0:
                del (new_graph[curr_node])

        new_curr_path = copy.deepcopy(curr_path)

        if target_node.islower() and is_eligible:
            # print("[{}] target node: {} is lower and eligible".format(lvl, target_node))
            generate_paths_to_end(new_graph, all_paths, new_curr_path, target_node, lvl + 1)
        elif target_node == "end" or (target_node.isupper() and target_node in new_graph):
            # print("[{}] target node: {} is end or is eligible".format(lvl, target_node))
            generate_paths_to_end(new_graph, all_paths, new_curr_path, target_node, lvl + 1)
        else:
            # print("[{}] target node: {} not in new graph or not eligible, continue...".format(lvl, target_node))
            continue

    return


def find_solution_a(input_graph: dict[str:list]) -> int:
    all_paths = list()
    curr_path = list()
    for curr_node_from_start in sorted(input_graph["start"]):
        # empty the curr path before cycle with new 1st order node
        del curr_path[:]
        curr_path.append("start")
        generate_paths_to_end(input_graph, all_paths, curr_path, curr_node_from_start)
        # print("all_paths so far: {}".format(all_paths))

    # print("all paths:\n{}".format(pprint.pformat(all_paths, indent=3, width=144)))

    return len(all_paths)


def find_solution_b():
    pass


def fill_paths_graph(input_data: list[str]) -> dict[str:list[str]]:
    new_initial_graph = dict()

    for line in input_data:
        left, right = line.split("-")

        # add direct path
        if right != "start":
            if left not in new_initial_graph:
                new_initial_graph[left] = [right]
            else:
                new_initial_graph[left].append(right)

        # the back path is added only for ordinary nodes (i.e. not "start" and "end")
        if left == "start" or right == "end":
            continue

        if right not in new_initial_graph:
            new_initial_graph[right] = [left]
        else:
            new_initial_graph[right].append(left)

    return new_initial_graph


def eliminate_invalid_paths(original_graph: dict[str:list]) -> dict[str:list[str]]:
    new_graph = original_graph.copy()

    # print("start new_graph:\n{}".format(pprint.pformat(new_graph)))
    for key in original_graph:
        if key.isupper() or key == "start":
            continue

        # process its lower connections
        lower_vals = [elem for elem in new_graph[key] if elem.islower()]

        if "end" in lower_vals:
            continue
        elif len(lower_vals) == 1:
            # this is dead end, remove both - current key and element from above
            # print("REM - key: {}, lower_vals: {}".format(key, lower_vals))
            new_graph[lower_vals[0]].remove(key)
            del (new_graph[key])

    # print("end new_graph:\n{}".format(pprint.pformat(new_graph)))

    return new_graph


def do_main():
    prev_time = time.process_time()

    print("start reading input...")
    data = read_input()
    cur_time = time.process_time()
    diff = cur_time - prev_time
    prev_time = cur_time
    print("[{}] took: {} sec.".format(cur_time, diff))

    # print("input data: {}".format(data))

    print("parse input and fill paths graph(dict)...")
    path_graph = fill_paths_graph(data)
    # print("path_graph:\n{}".format(pprint.pformat(path_graph, indent=3, sort_dicts=False)))
    cur_time = time.process_time()
    diff = cur_time - prev_time
    prev_time = cur_time
    print("[{}] took: {} sec.".format(cur_time, diff))

    # print("parse graph(dict) and eliminate invalid connections(paths)...")
    # reduced_graph = eliminate_invalid_paths(path_graph)
    # print("reduced_graph:\n{}".format(pprint.pformat(reduced_graph, indent=3, width=99)))
    # cur_time = time.process_time()
    # diff = cur_time - prev_time
    # prev_time = cur_time
    # print("[{}] took: {} sec.".format(cur_time, diff))

    print("find_solution_a...")
    # result_a = find_solution_a(reduced_graph.copy())
    result_a = find_solution_a(path_graph.copy())
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
    # prev_time = cur_time
    print("[{}] took: {} sec.".format(cur_time, diff))


if __name__ == "__main__":
    # execute only if run as a script

    filename = os.path.basename(__file__)
    day_nr = re.search(r"\d+", filename).group()
    print("day_nr:", day_nr)

    do_main()
