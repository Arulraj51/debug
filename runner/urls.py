from django.urls import path
from . import views
from django.contrib import admin
urlpatterns = [
    path('', views.index, name='index'),
    path('challenge/<int:id>/', views.challenge_view, name='challenge'),
    path('admin/', admin.site.urls),    
]
