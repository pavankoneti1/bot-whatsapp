from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RegisterUser
router = DefaultRouter()

router.register(r'', RegisterUser, basename='user_registration')

app_name = 'users'
urlpatterns = [
    path('', include(router.urls)),
]