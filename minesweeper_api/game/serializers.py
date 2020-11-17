from rest_framework import serializers
from game.models import Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'start_date', 'end_date', 'status', 'user', 'board']


class GameCreateSerializer(serializers.Serializer):
    starting_row = serializers.IntegerField()
    starting_column = serializers.IntegerField()
    number_of_mines = serializers.IntegerField()
    rows = serializers.IntegerField()
    columns = serializers.IntegerField()
