from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('driver/register/<int:user_id>/', views.DriverRegisterView.as_view(), name='driver_register'),
    path('admin/panel', views.AdminPanelView.as_view(), name='admin_panel'),
    path('admin/change/city', views.ChangeCityView.as_view(), name='change_city'),
    path('list_city/', views.ListCityView.as_view(), name='list_city'),
    path('driver/detail/', views.DriverDetailView.as_view(), name='driver_detail'),
    path('driver/travel/<int:user_id>/', views.TravelDriverInfo.as_view(), name='driver_travel'),
    
    path('driver/panel', views.DriverRegisterAdminView.as_view(), name='driver_panel'),
    path('admin/travels/', views.TravelRegisterView.as_view(), name='travel_admin'),
    path('travel/details/', views.TravelListView.as_view(), name='travel_detail'),
    path('delete/travel', views. DeleteTravelView.as_view(), name='delete_travel'),
    path('delete/city/', views.DeleteCityView.as_view(), name='delete_city'),
    path('driver/delete/', views.DeleteDriverView.as_view(), name='driver_delete'),
    path('driver/profile/<int:driver_id>/', views.DriverProfileView.as_view(), name='driver_profile'),
    path('driver/register/travel/<int:driver_id>/', views.DriverRegisterTravel.as_view(), name='driver_register_travel'),
    path('approve/travel/<int:travel_id>/', views.ApproveTravelAdminView.as_view(), name='approve_travel'),
    
    path('base/time/', views.BaseTimeView.as_view(), name='base_time'),
    path('base/price/', views.BasePriceView.as_view(), name='base_price'),
    path('price/list/', views.BasePriceList.as_view(), name='price_list'),
    path('car/register/', views.CarRegisterView.as_view(), name='car_register'),
    path('car/list/', views.CarListView.as_view(), name='car_list'),
    path('wallet/balance/', views.WalletBalanceListView.as_view(), name='wallet_balance'),
    path('wallet/add/amount/', views.AddAmountWalletView.as_view(), name='add_amount'),
    path('transection/list/', views.TransecitonListView.as_view(), name='transection_list'),
    path('transection/request/<int:transection_id>/', views.TransectionRequestListView.as_view(), name='transection_request'),
    path('user/transection/<int:user_id>/', views.TransectionLogListView.as_view(), name='user_transection'),
    path('submit/basepercent/', views.BasePercentView.as_view(), name='base_percent'),
]