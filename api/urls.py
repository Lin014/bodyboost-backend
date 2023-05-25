from django.urls import path
from .views import user_views, profile_views, authentication_views

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Bodyboost API",
      default_version='v1',
      description="Bodyboost API documentation"
   ),
   public=True,
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # users
    path('users/', user_views.getAllUser),
    path('users/<int:id>/', user_views.getUserById),
    path('users/add/', user_views.addUser),
    path('users/update/<int:id>/', user_views.updateUser),
    path('users/delete/<int:id>/', user_views.deleteUser),
    path('users/login/normal/', user_views.login_normal),
    path('users/login/google/', user_views.login_google),
    # authentication
    path('authentication/resendRegisterMail/<int:id>/', authentication_views.resendRegisterMail),
    path('authentication/sendForgetPasswordMail/', authentication_views.sendForgetPasswordMail),
    path('authentication/authenticationRegisterCode/', authentication_views.authenticationRegisterCode),
    path('authentication/authenticationForgetPasswordCode/', authentication_views.authenticationForgetPasswordCode),
    # profile
    path('profile/', profile_views.getAllProfile),
    path('profile/<int:id>/', profile_views.getProfileById),
    path('profile/add/', profile_views.addProfile),
    path('profile/update/<int:id>/', profile_views.updateProfile),
    path('profile/delete/<int:id>/', profile_views.deleteProfile),
]
