import random

VALUE_MINE = 'X'
VALUE_BLANK = 0
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
    board = [[{'value': VALUE_BLANK, 'status': STATUS_COVERED} for column in range(columns)] for row in range(rows)]

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

    if cell.get('value') != VALUE_BLANK:
        return

    #cell is blank
    adjacent_cells = get_adjacent_cells_coordinates(row, column, board)
    for adj_row, adj_column in adjacent_cells:
        uncover_cell(adj_row, adj_column, board)


def flag_cell(row, column, board):
    cell = board[row][column]

    if cell.get('status') == STATUS_UNCOVERED:
        return
    if cell.get('status') == STATUS_FLAGGED:
        cell['status'] = STATUS_COVERED
    else:
        cell['status'] = STATUS_FLAGGED


def winning(board):
    """ Return False if any non-mine cell is covered"""
    for row in board:
        for cell in row:
            if cell.get('status') in [STATUS_COVERED, STATUS_FLAGGED] and cell.get('value') != VALUE_MINE:
                return False
    return True
