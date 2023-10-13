from django.urls import path, include
from .views import home

app_name = 'tester'
urlpatterns = [
    path(r't/', home)
]