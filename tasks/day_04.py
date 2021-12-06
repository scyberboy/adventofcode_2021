import os
import re
import sys

marked = "x"
unmarked = "o"


def read_input():
    # read 1st line with bingo numbers
    line = sys.stdin.readline()
    bingo_numbers = [int(num.strip()) for num in line.strip().split(",")]

    # consume one empty
    line = sys.stdin.readline()

    # now the boards
    boards = list()
    board = list()
    row = dict()
    for line in sys.stdin:
        if line == "\n":
            boards.append(board)
            board = list()
            continue

        for val in line.strip().split():
            row[int(val)] = unmarked

        board.append(row)
        row = dict()

    # add the last board
    boards.append(board)

    return bingo_numbers, boards


def board_has_bingo(board):
    columned_board = list()

    for row_idx, row in enumerate(board):

        if unmarked not in row.values():
            # print("\tFound row bingo!")
            return True

        for elem_idx, _key in enumerate(row):
            # use new empty object
            new_col = dict()

            # for the first elements of the cols directly add
            if row_idx == 0:
                new_col[_key] = row[_key]
                columned_board.append(new_col)
                continue
            # for the rest - first load, add col element and update
            else:
                new_col = columned_board[elem_idx].copy()

            new_col[_key] = row[_key]
            columned_board[elem_idx] = new_col

    # traverse the just constructed cols for bingo
    for col in columned_board:
        if unmarked not in col.values():
            return True

    return False


def calc_sum_unmarked(board):
    sum_val = 0
    for row in board:
        for _key, _val in row.items():
            if _val == unmarked:
                sum_val += _key

    return sum_val


def find_first_bingo_board(number, boards):
    for board_idx, board in enumerate(boards):
        for row_idx, row in enumerate(board):
            if number in row:
                row[number] = marked
                board[row_idx] = row
                if board_has_bingo(board):
                    return board, board_idx

    return None, -1


def find_last_bingo_board(number, boards):
    last_bingo_board = None
    last_bingo_idx = -1
    for board_idx, board in enumerate(boards):
        for row_idx, row in enumerate(board):
            if number in row:
                row[number] = marked
                board[row_idx] = row
                if board_has_bingo(board):
                    last_bingo_board = board.copy()
                    last_bingo_idx = board_idx
                    # we should traverse all remaining boards for the current number
                    # but first clean-up the current winning one
                    boards[board_idx].clear()
                    continue

    return last_bingo_board, last_bingo_idx


def find_solution_a(numbers, boards):
    # Find the first winning board

    for number in numbers:
        bingo_board, bingo_board_idx = find_first_bingo_board(number, boards)
        if bingo_board:
            sum_unmarked = calc_sum_unmarked(bingo_board)
            answer = number * sum_unmarked
            # print("answer: {} <- number: {}, sum_unmarked: {}".format(answer, number, sum_unmarked))
            return answer

    return None


def find_solution_b(numbers, boards):
    # Find the last winning board

    last_winning_board = list()
    last_winning_num = -1

    for number in numbers:
        bingo_board, bingo_board_idx = find_last_bingo_board(number, boards)
        if bingo_board is not None and bingo_board_idx >= 0:
            # always copy list elements, otherwise a ref is kept (which can later be altered)
            last_winning_board = bingo_board.copy()
            last_winning_num = number
            # clear any bingo boards' content, so it's not in the game anymore
            boards[bingo_board_idx].clear()

    sum_unmarked = calc_sum_unmarked(last_winning_board)
    answer = last_winning_num * sum_unmarked
    # print("answer: {} <- number: {}, sum_unmarked: {}".format(answer, last_winning_num, sum_unmarked))
    return answer


def do_main():

    numbers, boards = read_input()
    print("numbers:", numbers)
    print("nr. boards:", len(boards))

    result_a = find_solution_a(numbers, boards)
    print("result_a:", result_a)

    result_b = find_solution_b(numbers, boards)
    print("result_b:", result_b)


if __name__ == "__main__":
    # execute only if run as a script

    filename = os.path.basename(__file__)
    day_nr = re.search(r"\d+", filename).group()
    print("day_nr:", day_nr)

    do_main()
