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


def generate_paths_to_end(inner_graph: dict[str:list[str]], curr_node: str, lvl=0) -> list[list[str]]:
    curr_path = list()
    inner_paths = list()

    print("[{}] curr_node: {} -> inner_graph({}): {}".format(lvl, curr_node, id(inner_graph), pprint.pformat(inner_graph)))

    if curr_node == "end":
        return ["end"]

    for target_node in inner_graph[curr_node]:
        new_graph = copy.deepcopy(inner_graph)
        new_graph[curr_node].remove(target_node)
        if len(new_graph[curr_node]) == 0:
            del(new_graph[curr_node])

        # print("[{}] target node: {}".format(lvl, target_node))
        inner_path = generate_paths_to_end(new_graph, target_node, lvl+1)
        print("[{}] inner calls generated inner_path: {}".format(lvl, inner_path))

        # tuka trqa dobavqm cur_path/cur_node wyw nachaloto na wseki inner_path !
        if isinstance(inner_path[0], str):
            inner_path.insert(0, curr_node)
        else:
            for elem in inner_path:
                elem.insert(0, curr_node)

        print("[{}] inner PAT become: {}".format(lvl, inner_path))

        inner_paths.append(inner_path)
        print("[{}] inner_pathS become: {}".format(lvl, inner_paths))


    curr_path = inner_paths.copy()
    print("[{}] curr path: {}".format(lvl, pprint.pformat(curr_path)))

    return curr_path


def find_solution_a(input_graph: dict[str:list]) -> int:

    all_paths = list()
    for blah in input_graph["start"]:
        paths_to_end = generate_paths_to_end(input_graph, blah)
        print("PATHs to END for {}:\n{}".format(blah, paths_to_end))
        all_paths.extend(paths_to_end)

    print("all paths:\n{}".format(pprint.pformat(all_paths, indent=3)))

    return len(all_paths)


def find_solution_b():
    pass


def fill_paths_graph(input_data: list[str]) -> dict[str:list[str]]:
    new_initial_graph = dict()

    for line in input_data:
        left, right = line.split("-")

        # add direct path
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
            del(new_graph[key])

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
    print("path_graph:\n{}".format(pprint.pformat(path_graph)))
    cur_time = time.process_time()
    diff = cur_time - prev_time
    prev_time = cur_time
    print("[{}] took: {} sec.".format(cur_time, diff))

    print("parse graph(dict) and eliminate invalid connections(paths)...")
    reduced_graph = eliminate_invalid_paths(path_graph)
    print("reduced_graph:\n{}".format(pprint.pformat(reduced_graph)))
    cur_time = time.process_time()
    diff = cur_time - prev_time
    prev_time = cur_time
    print("[{}] took: {} sec.".format(cur_time, diff))

    print("find_solution_a...")
    result_a = find_solution_a(reduced_graph.copy())
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
