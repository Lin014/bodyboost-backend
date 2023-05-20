from django.urls import path, include
from . import views

urlpatterns = [
    path('users/', views.getUsers),
    path('users/add/', views.addUser)
]
