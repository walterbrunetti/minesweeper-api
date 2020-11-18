from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from game.models import Game
from game.serializers import GameSerializer, GameCreateSerializer


class GamePortalView(TemplateView):
    template_name = "game/game.html"


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_queryset(self):
        user = self.request.user
        return Game.objects.filter(user=user)

    def create(self, request):
        user = self.request.user
        create_serializer = GameCreateSerializer(data=request.data)

        if create_serializer.is_valid():
            game = Game.objects.create_new(user, **create_serializer.data)
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def uncover_cell(self, request, pk):
        row = request.data.get('row')
        column = request.data.get('column')

        game = get_object_or_404(self.queryset, pk=pk)
        game.uncover_cell(row, column)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def flag_cell(self, request, pk):
        row = request.data.get('row')
        column = request.data.get('column')

        game = get_object_or_404(self.queryset, pk=pk)
        game.flag_cell(row, column)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def pause(self, request, pk):
        game = get_object_or_404(self.queryset, pk=pk)
        game.pause()
        serializer = GameSerializer(game)
        return Response(serializer.data)
