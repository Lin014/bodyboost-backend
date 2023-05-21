from django.urls import path, include
from .views import user_views

urlpatterns = [
    path('users/', user_views.getUsers),
    path('users/<int:id>/', user_views.getUserById),
    path('users/add/', user_views.addUser),
    path('users/update/<int:id>/', user_views.updateUser),
    path('users/delete/<int:id>/', user_views.deleteUser),
    path('users/login/normal', user_views.login_normal),
    path('users/login/google', user_views.login_google)
]
