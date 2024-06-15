from django.urls import path
from . import views


app_name = 'travels'
urlpatterns = [
    path('admin/travels/', views.TravelRegisterView.as_view(), name='travel_admin'),
    path('delete/travel', views. DeleteTravelView.as_view(), name='delete_travel'),
    path('approve/travel/<int:travel_id>/', views.ApproveTravelAdminView.as_view(), name='approve_travel'),
    path('register/travel/<int:driver_id>/', views.DriverRegisterTravel.as_view(), name='driver_register_travel'),
    path('travel/details/', views.TravelListView.as_view(), name='travel_detail'),
    path('ticket/detail/<int:travel_id>/', views.TicketListAdminView.as_view(), name='ticket_list'),
    path('travel/list/ticket/', views.TravelListTicketView.as_view(), name='travel_list_admin'),
    path('ticket/info/<int:travel_id>/', views.TravelDetailUserView.as_view(), name='ticket_detail'),
    
]