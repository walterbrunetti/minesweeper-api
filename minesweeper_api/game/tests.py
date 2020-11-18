from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework import status
from engine.engine import VALUE_BLANK, STATUS_COVERED
from game.models import Game, STATUS_IN_PROGRESS
from game.serializers import GameSerializer


class SerializerTests(TestCase):
    def setUp(self):
        self.board = [
            [{'value': VALUE_BLANK, 'status': STATUS_COVERED}, {'value': VALUE_BLANK, 'status': STATUS_COVERED}],
            [{'value': VALUE_BLANK, 'status': STATUS_COVERED}, {'value': VALUE_BLANK, 'status': STATUS_COVERED}]
        ]
        self.user = User.objects.create_user(username='walter', password='test', is_superuser=True)
        self.game = Game.objects.create(user=self.user, board=self.board, status=STATUS_IN_PROGRESS)

    def test_serializer_serialize_game_object_correctly(self):
        expected_data = {
            'id': self.game.id,
            'start_date': self.game.start_date.strftime("%m/%d/%Y %H:%M:%S"),
            'status': self.game.status,
            'user': self.game.user.id,
            'time_elapsed': self.game.time_elapsed,
            'status_description': 'In Progress',
            'board': self.game.board
        }

        serialized_data = GameSerializer(self.game)
        self.assertEquals(serialized_data.data, expected_data)


class GameViewSetTests(TestCase):

    def setUp(self):
        self.board = [
            [{'value': VALUE_BLANK, 'status': STATUS_COVERED}, {'value': VALUE_BLANK, 'status': STATUS_COVERED}],
            [{'value': VALUE_BLANK, 'status': STATUS_COVERED}, {'value': VALUE_BLANK, 'status': STATUS_COVERED}]
        ]
        self.user = User.objects.create_user(username='walter', password='test', is_superuser=True)
        self.game = Game.objects.create(user=self.user, board=self.board, status=STATUS_IN_PROGRESS)
        self.client = Client(HTTP_POST='localhost')
        self.client.login(username='walter', password='test')

    def test_only_logged_id_user_games_are_returned(self):
        other_user = User.objects.create_user(username='user1', password='test', is_superuser=True)
        Game.objects.create(user=other_user, board=self.board, status=STATUS_IN_PROGRESS)

        response = self.client.get('/game/')

        serialized_data = GameSerializer(self.game)
        self.assertEquals(response.json(), [serialized_data.data])

    def test_game_is_created_successfully_if_correct_data_is_sent(self):
        starting_row = 0
        starting_column = 0
        number_of_mines = 5
        rows = 10
        columns = 15

        response = self.client.post('/game/', {'starting_row': starting_row, 'starting_column': starting_column,
                                               'number_of_mines': number_of_mines, 'rows': rows, 'columns': columns})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_fails_if_any_value_is_not_a_number(self):
        starting_row = 0
        starting_column = 0
        number_of_mines = 'not a number'
        rows = 10
        columns = 15

        response = self.client.post('/game/', {'starting_row': starting_row, 'starting_column': starting_column,
                                               'number_of_mines': number_of_mines, 'rows': rows, 'columns': columns})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"number_of_mines":["A valid integer is required."]}')
