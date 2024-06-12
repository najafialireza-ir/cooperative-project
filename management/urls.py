from django.urls import path
from . import views

app_name = 'app_name'
urlpatterns = [
    path('admin/panel', views.AdminPanelView.as_view(), name='admin_panel'),
    path('admin/change/city', views.ChangeCityView.as_view(), name='change_city'),
    path('list_city/', views.ListCityView.as_view(), name='list_city'),
    path('driver/detail/', views.DriverDetailView.as_view(), name='driver_detail'),
    path('driver/panel', views.DriverRegisterAdminView.as_view(), name='driver_register_admin'),
    path('base/time/', views.BaseTimeView.as_view(), name='base_time'),
    path('base/price/', views.BasePriceView.as_view(), name='base_price'),
    path('price/list/', views.BasePriceList.as_view(), name='price_list'),
    path('car/register/', views.CarRegisterView.as_view(), name='car_register'),
    path('car/list/', views.CarListView.as_view(), name='car_list'),
    path('delete/city/', views.DeleteCityView.as_view(), name='delete_city'),
    path('driver/delete/', views.DeleteDriverView.as_view(), name='driver_delete'),
    path('submit/basepercent/', views.BasePercentView.as_view(), name='base_percent'),
    path('base/refund/', views.BaseTimeRefundView.as_view(), name='base_time_refund'),
    path('base/time/refund/list', views.BaseTimeRefundList.as_view(), name='base_time_refund_list'),
    path('base/percent/list/', views.BasePercentListView.as_view(), name='base_percent_list'),
    
    
]