from django.urls import path
from . import views

urlpatterns = [
    path('identify_image/', views.identify_image, name='identify_image'),
    
]