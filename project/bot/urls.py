from django.urls import path, include

from rest_framework import routers
from .views import BotViewset

router = routers.DefaultRouter()
router.register('', BotViewset, basename='bot')

app_name = 'bot'
urlpatterns = [
    path('', include(router.urls)),
]