from django.urls import path
from . import views

app_name = 'wallet'
urlpatterns = [
    path('wallet/add/amount/', views.AddAmountWalletView.as_view(), name='add_amount'),
    path('transection/list/', views.TransecitonListView.as_view(), name='transection_list'),
    path('transection/request/<int:transection_id>/', views.TransectionRequestListView.as_view(), name='transection_request'),
    path('user/transection/<int:user_id>/', views.TransectionLogListView.as_view(), name='user_transection'),
    path('wallet/balance/', views.WalletBalanceListView.as_view(), name='wallet_balance'),
    
]