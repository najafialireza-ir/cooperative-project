from django.urls import path
from . import views


app_name = 'orders'
urlpatterns = [
    path('add/orders/<int:travel_id>/', views.AddOrderView.as_view(), name='add_order'),
    path('orders/detail/<int:user_id>/', views.CartListView.as_view(), name='cart_list'),
    path('order/delete/', views.CartDeleteView.as_view(), name='order_delete'),
    path('ticket/detail/<int:ticket_id>/', views.TicketListUserView.as_view(), name='ticket_lsit_user'),
    path('order/pay/<int:user_id>/', views.OrderPayView.as_view(), name='order_pay'),
    path('purchased/list<int:user_id>/', views.PurchasedListView.as_view(), name='purchased_list'),
    path('purchase/delete/', views.PurchasedDeleteView.as_view(), name='purchase_delete'),
]