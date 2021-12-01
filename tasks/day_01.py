import sys
import os
import re

input_data = []

filename = os.path.basename(__file__)
day_nr = re.search(r"\d+", filename).group()
print("day_nr:", day_nr)


def read_input():
    for line in sys.stdin:
        input_data.append(int(line.strip()))


def do_main():

    read_input()
    print(input_data)

if __name__ == "__main__":
    # execute only if run as a script
    do_main()
