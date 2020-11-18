import sys
from engine import start_new_board, uncover_cell, winning, MineExplodedException, STATUS_UNCOVERED


def print_board(board):
    print("  " + " ".join(str(x) for x in range(len(board[0]))))
    for i, row in enumerate(board):
        print("{}|".format(i) + " ".join(str(cell.get('value') if cell.get('status') == STATUS_UNCOVERED else '#') for cell in row))
        print("")


def main():
    number_of_rows = 15
    number_of_columns = 10
    number_of_mines = 15
    board = None

    while True:
        selected_row, selected_column = input("Enter coordinates comma-separated: ").split(',')

        # TODO: validate input
        # TODO: accept flag input

        if not board:
            board = start_new_board(number_of_mines, number_of_rows, number_of_columns, int(selected_row), int(selected_column))
            print_board(board)

        try:
            uncover_cell(int(selected_row), int(selected_column), board)
        except MineExplodedException:
            print('Boom! game is over :(')
            sys.exit()

        print('============================')
        print_board(board)

        if winning(board):
            print('Congrats! You won!')
            sys.exit()


if __name__ == "__main__":
    main()
