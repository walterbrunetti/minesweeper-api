from django.db import models
from django.contrib.auth.models import User


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


class Game(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    time_elapsed = models.IntegerField(default=0)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    board = models.JSONField()
