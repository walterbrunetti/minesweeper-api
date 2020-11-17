from django.urls import path, include
from rest_framework import routers
from game.views import GameViewSet


router = routers.DefaultRouter()
router.register(r'game', GameViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
