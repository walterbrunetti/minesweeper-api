from rest_framework import serializers
from game.models import Game


class GameSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(format='%m/%d/%Y %H:%M:%S')
    status_description = serializers.SerializerMethodField()

    def get_status_description(self, obj):
        return obj.get_status_display()

    class Meta:
        model = Game
        fields = ['id', 'start_date', 'status', 'user', 'time_elapsed', 'status_description', 'board']


class GameCreateSerializer(serializers.Serializer):
    starting_row = serializers.IntegerField()
    starting_column = serializers.IntegerField()
    number_of_mines = serializers.IntegerField()
    rows = serializers.IntegerField()
    columns = serializers.IntegerField()
