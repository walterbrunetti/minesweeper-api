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



"""
Y
|
V 0 1 2 3   <-- X
0 1 M 1 E
1 2 1 1 E
2 1 M X 1
3 1 2 M 1

Getting adjacents sqares:
(x,y) | (2,2): (1,2) (3,2)  --> (x-1,y) (x+1,y)
               (2,1) (2,3)  --> (x,y-1) (x,y+1)
               (1,1) (3,1) (1,3) (3,3) --> corners  --> (x-1,y-1) (x+1,y-1) (x-1,y+1) (x+1,y+1)


Game rules:
- If a player uncovers a mined cell, the game ends.
- Otherwise, the uncovered cells displays either a number, indicating the quantity of mines adjacent to it, or a blank tile.
- all adjacent non-mined cells will automatically be uncovered.
- The first click in any game will never be a mine.
- To win the game, players must uncover all non-mine cells, at which point the timer is stopped.


How program would work:
1- Create a grid with given number of rows, columns
2- Place mines
3- For each mined cell, add 1 to the adjacent cells
4- When a cell is uncovered, if it's a mine the game ends.
5- Otherwise, uncovered cell displays either a number, indicating the quantity of mines adjacent to it, or a blank tile.
6- If it's a blank cell, uncover all the adjacent cells.
7- For each blank cell uncovered, repeat the process from #5.


Open questions:
- when counting adjacent mined cells? During playing/uncovering cells? or all at once on starting?




"""
