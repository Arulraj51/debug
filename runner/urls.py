from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('challenge/<int:id>/', views.challenge_view, name='challenge'),
]