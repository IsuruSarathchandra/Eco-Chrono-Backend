# yourappname/urls.py
from django import views
from django.urls import path
from .views import get_tree_details

urlpatterns = [
    path('<str:title>/<str:circumference>/',get_tree_details),
]
