import sys
import os
import re

input_data = []

filename = os.path.basename(__file__)
day_nr = re.search(r"\d+", filename).group()
print("day_nr:", day_nr)

# forward(+) command
horizontal = 0  # part a, b: +

# down(+)/up(-) commands
depth = 0
# part a: +/-
# part b: += aim * fwd (on forward command)

aim = 0  # part b: +/-


def read_input():
    for line in sys.stdin:
        cmd_val_list = line.strip().split()
        input_data.append({"cmd": cmd_val_list[0],
                           "val": int(cmd_val_list[1])})


def find_solution_a():
    global horizontal
    global depth

    for instr in input_data:
        if instr["cmd"] == "forward":
            horizontal += instr["val"]
        elif instr["cmd"] == "down":
            depth += instr["val"]
        elif instr["cmd"] == "up":
            depth -= instr["val"]
        else:
            print("BATAMATA - unknown cmd".format(instr["cmd"]))

    # print("horizontal:", horizontal, "depth:", depth)
    result = horizontal * depth
    return result


def find_solution_b():
    global horizontal
    global depth
    global aim

    for instr in input_data:
        if instr["cmd"] == "forward":
            horizontal += instr["val"]
            depth += aim * instr["val"]
        elif instr["cmd"] == "down":
            aim += instr["val"]
        elif instr["cmd"] == "up":
            aim -= instr["val"]
        else:
            print("BATAMATA - unknown cmd".format(instr["cmd"]))

    # print("horizontal:", horizontal, "depth:", depth, "aim:", aim)
    result = horizontal * depth

    return result


def do_main():
    global horizontal
    global depth

    read_input()
    # print("input_data", input_data)
    # print("horizontal:", horizontal, "depth:", depth)

    result_a = find_solution_a()
    print("result_a:", result_a)
    # print("horizontal:", horizontal, "depth:", depth)

    horizontal = 0
    depth = 0
    result_b = find_solution_b()
    print("result_b:", result_b)


if __name__ == "__main__":
    # execute only if run as a script
    do_main()
