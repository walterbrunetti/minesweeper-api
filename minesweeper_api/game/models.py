from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from engine.engine import start_new_board, uncover_cell, MineExplodedException, winning, flag_cell


STATUS_IN_PROGRESS = 1
STATUS_PAUSED = 2
STATUS_COMPLETED_WIN = 3
STATUS_COMPLETED_LOSE = 4

STATUS_CHOICES = [
    (STATUS_IN_PROGRESS, 'In Progress'),
    (STATUS_PAUSED, 'Paused'),
    (STATUS_COMPLETED_WIN, 'Completed - win'),
    (STATUS_COMPLETED_LOSE, 'Completed - lose')
]


class GameManager(models.Manager):
    def create_new(self, user, starting_row, starting_column, number_of_mines, rows, columns):
        board = start_new_board(number_of_mines, rows, columns, starting_row, starting_column)
        uncover_cell(starting_row, starting_column, board)

        game = Game(user=user, board=board, status=STATUS_IN_PROGRESS)
        game.save()
        return game


class Game(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    time_elapsed = models.IntegerField(default=0)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    board = models.JSONField()

    objects = GameManager()

    def uncover_cell(self, row, column):
        board = self.board
        try:
            uncover_cell(row, column, board)

            if winning(board):
                self.status = STATUS_COMPLETED_WIN
                self.end_date = datetime.now()
        except MineExplodedException:
            self.status = STATUS_COMPLETED_LOSE
            self.end_date = datetime.now()

        self.board = board
        self.save()

    def flag_cell(self, row, column):
        flag_cell(row, column, self.board)
        self.save()

    def pause(self):
        self.status = STATUS_PAUSED
        self.save()
