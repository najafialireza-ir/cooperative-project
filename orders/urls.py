from django.urls import path
from . import views


app_name = 'orders'
urlpatterns = [
    path('ticket/info/<int:travel_id>/', views.TravelDetailUserView.as_view(), name='ticket_detail'),
    path('add/orders/<int:travel_id>/', views.AddOrderView.as_view(), name='add_order'),
    path('orders/detail/<int:user_id>/', views.OrderDetailView.as_view(), name='orders_detail'),
    path('order/delete/', views.OrderDeleteView.as_view(), name='order_delete')
    
]