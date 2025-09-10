from django.contrib import admin
from django.urls import path

from .views import *  # noqa: F403


urlpatterns = [
    path('', index),  # noqa: F405
    path('cats/', categories),
]