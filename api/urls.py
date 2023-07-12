from django.urls import path
from django.conf.urls.static import static

from .views import dailybonus_views, dietrecord_views, user_views, profile_views, authentication_views, store_views, foodtype_views, food_views, customfood_views

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from bodyboost.settings import MEDIA_URL, MEDIA_ROOT

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
    path('authentication/resendRegisterMail/', authentication_views.resendRegisterMail),
    path('authentication/sendForgetPasswordMail/', authentication_views.sendForgetPasswordMail),
    path('authentication/authenticationRegisterCode/', authentication_views.authenticationRegisterCode),
    path('authentication/authenticationForgetPasswordCode/', authentication_views.authenticationForgetPasswordCode),
    # profile
    path('profile/', profile_views.getAllProfile),
    path('profile/<int:id>/', profile_views.getProfileById),
    path('profile/add/', profile_views.addProfile),
    path('profile/update/<int:id>/', profile_views.updateProfile),
    path('profile/delete/<int:id>/', profile_views.deleteProfile),
    path('profile/uploadProfileImage/<int:id>', profile_views.uploadProfileImage),
    # dailybonus
    path('dailybonus/<int:id>/', dailybonus_views.getDailyBonusById),
    path('dailybonus/add/<int:id>/', dailybonus_views.addDailyBonusById),
    # store
    path('store/', store_views.getAllStore),
    path('store/add/', store_views.addStore),
    path('store/update/<int:id>', store_views.updateStore),
    path('store/delete/<int:id>', store_views.deleteStore),
    # foodtype
    path('foodtype/', foodtype_views.getAllFoodType),
    path('foodtype/add/', foodtype_views.addFoodType),
    path('foodtype/update/<int:id>', foodtype_views.updateFoodType),
    path('foodtype/delete/<int:id>', foodtype_views.deleteFoodType),
   # food
   path('food/', food_views.getAllFood),
   path('food/add/', food_views.addFood),
   path('food/update/<int:id>', food_views.updateFood),
   path('food/delete/<int:id>', food_views.deleteFood),
   # customfood
   path('customfood/', customfood_views.getAllCustomFood),
   path('customfood/add/', customfood_views.addCustomFood),
   path('customfood/update/<int:id>', customfood_views.updateCustomFood),
   path('customfood/delete/<int:id>', customfood_views.deleteCustomFood),
   # dietrecord
   path('dietrecord/<int:id>', dietrecord_views.getDietRecordById),
   path('dietrecord/add/', dietrecord_views.addDietRecord),
   path('dietrecord/update/<int:id>', dietrecord_views.updateDietRecord),
   path('dietrecord/delete/<int:id>', dietrecord_views.deleteDietRecord),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
