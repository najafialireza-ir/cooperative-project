from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('driver/register/<int:user_id>/', views.DriverRegisterView.as_view(), name='driver_register'),
    path('driver/travel/<int:user_id>/', views.TravelDriverInfo.as_view(), name='driver_travel'),
    path('driver/profile/<int:driver_id>/', views.DriverProfileView.as_view(), name='driver_profile'),
]
   
 
   