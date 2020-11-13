import unittest
from engine.minesweeper_engine_terminal_based import place_mines, get_adjacent_cells_coordinates, uncover_cell, \
    BLANK, VALUE_MINE, STATUS_COVERED, STATUS_UNCOVERED, MineExplodedException


class EngineTestCase(unittest.TestCase):
    def setUp(self):
        self.board = [
            [{'value': BLANK, 'status': STATUS_COVERED}, {'value': BLANK, 'status': STATUS_COVERED},
             {'value': BLANK, 'status': STATUS_COVERED}, {'value': BLANK, 'status': STATUS_COVERED}],
            [{'value': BLANK, 'status': STATUS_COVERED}, {'value': BLANK, 'status': STATUS_COVERED},
             {'value': BLANK, 'status': STATUS_COVERED}, {'value': BLANK, 'status': STATUS_COVERED}],
            [{'value': BLANK, 'status': STATUS_COVERED}, {'value': BLANK, 'status': STATUS_COVERED},
             {'value': BLANK, 'status': STATUS_COVERED}, {'value': BLANK, 'status': STATUS_COVERED}],
            [{'value': BLANK, 'status': STATUS_COVERED}, {'value': BLANK, 'status': STATUS_COVERED},
             {'value': BLANK, 'status': STATUS_COVERED}, {'value': BLANK, 'status': STATUS_COVERED}],
            [{'value': BLANK, 'status': STATUS_COVERED}, {'value': BLANK, 'status': STATUS_COVERED},
             {'value': BLANK, 'status': STATUS_COVERED}, {'value': BLANK, 'status': STATUS_COVERED}]
        ]  # 5x4 array

    def test_get_adjacent_cells_coordinates_returns_only_adjacent_cells(self):
        row = 2
        column = 2
        expected_adjacent_cells = [(row-1, column), (row+1, column), (row, column-1), (row, column+1),
                                   (row-1, column-1), (row+1, column-1), (row-1, column+1), (row+1, column+1)]

        adjacent_cells = get_adjacent_cells_coordinates(row, column, self.board)
        self.assertEqual(adjacent_cells, expected_adjacent_cells)

    def test_get_adjacent_cells_coordinates_does_not_return_cells_outside_the_matrix(self):
        row = 0
        column = 0
        expected_adjacent_cells = [(1, 0), (0, 1), (1, 1)]

        adjacent_cells = get_adjacent_cells_coordinates(row, column, self.board)
        self.assertEqual(adjacent_cells, expected_adjacent_cells)

    def test_place_mines_returns_cells_with_mines(self):
        number_of_mines = 2
        starting_row = 2
        starting_column = 2

        cells_with_mines = place_mines(number_of_mines, self.board, starting_row, starting_column)

        for row, column in cells_with_mines:
            self.assertEqual(self.board[row][column].get('value'), VALUE_MINE)

    def test_place_mines_does_not_place_mines_on_starting_cell_coordinates(self):
        pass

    def test_uncover_cell_changes_status_to_uncover_if_value_is_a_number(self):
        row = 2
        column = 2

        cell = self.board[row][column]
        cell['value'] = 2
        cell['status'] = STATUS_COVERED

        uncover_cell(row, column, self.board)

        cell = self.board[row][column]
        self.assertEqual(cell.get('status'), STATUS_UNCOVERED)

    def test_uncover_cell_changes_status_to_uncover_and_raise_exception_if_value_is_a_mine(self):
        row = 2
        column = 2

        cell = self.board[row][column]
        cell['value'] = VALUE_MINE
        cell['status'] = STATUS_COVERED

        with self.assertRaises(MineExplodedException) as context:
            uncover_cell(row, column, self.board)

        self.assertEqual('Boom!', str(context.exception))
        cell = self.board[row][column]
        self.assertEqual(cell.get('status'), STATUS_UNCOVERED)
