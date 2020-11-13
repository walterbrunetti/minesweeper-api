
import random
import sys

VALUE_MINE = 'X'
BLANK = 0
STATUS_COVERED = 'c'
STATUS_UNCOVERED = 'u'
STATUS_FLAGGED = 'F'


class MineExplodedException(Exception):
    pass


def place_mines(number_of_mines, board, starting_row, starting_column):
    """
    Randomly place mines, avoiding to place one in the starting coordinates and adjacent
    """
    max_row = len(board)
    max_column = len(board[0])

    adjacent_cells = get_adjacent_cells_coordinates(starting_row, starting_column, board)
    adjacent_cells.append((starting_row, starting_column))
    adjacent_cells = set(adjacent_cells)

    mined_cells = []

    count = 0
    while count < number_of_mines:
        random_row = random.randint(0,max_row-1)
        random_column = random.randint(0, max_column-1)
                
        if (random_row, random_column) in adjacent_cells:
            continue  # do not place here

        cell = board[random_row][random_column]
        if cell.get('value') == VALUE_MINE:
            continue

        cell['value'] = VALUE_MINE
        count += 1
        mined_cells.append((random_row, random_column))

    return mined_cells


def get_adjacent_cells_coordinates(row, column, board):
    max_row = len(board)
    max_column = len(board[0])

    adjacent_cells_coordinates = [(row-1, column), (row+1, column), (row, column-1), (row, column+1),
                                  (row-1, column-1), (row+1, column-1), (row-1, column+1), (row+1, column+1)]
    
    adjacent_cells_coordinates[:] = [tup for tup in adjacent_cells_coordinates if 0 <= tup[0] < max_row and 0 <= tup[1] < max_column]
    return adjacent_cells_coordinates


def add_1_to_cells(cells, board):
    for row, column in cells:
        cell = board[row][column]
        if cell.get('value') == VALUE_MINE:
            continue
        cell['value'] += 1


def start_new_board(number_of_mines, rows, columns, starting_row, starting_column):
    board = [[{'value': BLANK, 'status': STATUS_COVERED} for row in range(rows)] for column in range(columns)]
    
    # TODO: check number_of_mines fit in array
    
    mined_cells = place_mines(number_of_mines, board, starting_row, starting_column)

    for row, column in mined_cells:
        adjacent_cells = get_adjacent_cells_coordinates(row, column, board)
        add_1_to_cells(adjacent_cells, board)

    return board


def uncover_cell(row, column, board):
    cell = board[row][column]

    if cell.get('status') == STATUS_UNCOVERED:
        return

    cell['status'] = STATUS_UNCOVERED

    if cell.get('value') == VALUE_MINE:
        raise MineExplodedException('Boom!')

    if cell.get('value') != BLANK:
        return

    #cell is blank
    adjacent_cells = get_adjacent_cells_coordinates(row, column, board)
    for adj_row, adj_column in adjacent_cells:
        uncover_cell(adj_row, adj_column, board)


def flag_cell():
    # Add a flag if the cell is empty
    pass


def winning(board):
    #check if any non-mine cell is covered
    for row in board:
        pass
    return False


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
