from django.urls import path
from . import views
from .views import create_ad

urlpatterns = [
    path('create_ad/', views.create_ad, name='create_ad'),
    
]