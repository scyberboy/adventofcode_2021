import os
import re
import sys
import time

penalty_score = {")": 3,
                 "]": 57,
                 "}": 1197,
                 ">": 25137}

completion_score = {")": 1,
                    "]": 2,
                    "}": 3,
                    ">": 4}

openings = {"(": ")", "[": "]", "{": "}", "<": ">"}
closings = {")": "(", "]": "[", "}": "{", ">": "<"}


def read_input() -> list[str]:
    """

    :return:
    """
    # Read lines input:
    # [({(<(())[]>[[{[]{<()<>>
    # [(()[<>])]({[<{<<[]>>(
    # {([(<{}[<>[]}>{[]{[(<()>
    # (((({<>}<{<{<>}{[]{[]{}

    return [line.strip() for line in sys.stdin]


def calc_syntax_error_score(culprits: list[str]) -> int:
    global penalty_score
    score = 0
    for elem in culprits:
        score += penalty_score[elem]

    return score


def check_line_corrupted(line: str) -> (bool, str):
    global openings, closings
    syntax_stack = list()
    for elem in line:
        if elem in openings:
            syntax_stack.append(elem)
        else:
            anti_elem = syntax_stack.pop()
            if closings[elem] != anti_elem:
                return True, elem

    return False, ""


def find_solution_a(input_data: list[str]) -> int:
    culprits = list()
    for line in input_data:
        is_corrupted, culprit = check_line_corrupted(line)
        if is_corrupted:
            culprits.append(culprit)

    answer = -1
    if len(culprits) > 0:
        answer = calc_syntax_error_score(culprits)

    return answer


def calc_score(line: str) -> int:
    global completion_score
    total_chunk_score = 0
    for elem in line:
        total_chunk_score *= 5
        total_chunk_score += completion_score[elem]

    return total_chunk_score


def generate_score_list(completion: list[str]) -> list[int]:
    scores = list()
    for line in completion:
        scores.append(calc_score(line))

    return scores


def generate_completion_chunk(line: str) -> str:
    comp_chunk = ""
    incomp_stack = list()

    # print("incomp line: {}".format(list(line)))
    # fist process and drop correct stuff
    for elem in line:
        if elem in openings:
            incomp_stack.append(elem)
        else:
            # incomp_stack.remove(closings[elem])
            incomp_stack.pop()

    # print("incomp chunk: {}".format(incomp_stack))

    while len(incomp_stack) > 0:
        elem = incomp_stack.pop()
        comp_chunk += openings[elem]

    # print("comp chunk: {}".format(list(comp_chunk)))

    return comp_chunk


def find_solution_b(input_data: list[str]) -> int:
    incomplete = list()
    for line in input_data:
        is_corrupted, culprit = check_line_corrupted(line)
        if not is_corrupted:
            incomplete.append(line)

    # print("incomplete list: {}".format(incomplete))
    completion = list()
    for line in incomplete:
        completion.append(generate_completion_chunk(line))

    score_list = generate_score_list(completion)
    # print("score list: {}".format(score_list))
    middle_one = len(score_list) // 2

    answer = sorted(score_list)[middle_one]

    return answer


def do_main():
    prev_time = time.process_time()

    print("start reading input...")
    data = read_input()
    # print("input data: {}".format(data))
    cur_time = time.process_time()
    diff = cur_time - prev_time
    prev_time = cur_time
    print("[{}] took: {} sec.".format(cur_time, diff))

    # print("input data: {}".format(data))

    print("find_solution_a...")
    result_a = find_solution_a(data)
    print("result_a:", result_a)
    cur_time = time.process_time()
    diff = cur_time - prev_time
    prev_time = cur_time
    print("[{}] took: {} sec.".format(cur_time, diff))

    print("find_solution_b...")
    result_b = find_solution_b(data)
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
