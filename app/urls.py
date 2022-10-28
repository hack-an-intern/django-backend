from django.urls import path
from django.urls import include
from app import views
urlpatterns = [
    path('', views.index, name='index'),
]
