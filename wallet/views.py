from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TransectionLog, TransectionRequest
from management.models import BasePercent
from utils import IsAdmin
from django.contrib import messages
from .forms import AddAmountWalletForm


class AddAmountWalletView(LoginRequiredMixin, View):
    class_form = AddAmountWalletForm
    def get(self, request, *args, **kwargs):
        add_amount_form = self.class_form
        return render(request, 'wallet/add_amount_wallet_form.html', {'add_amount_form':add_amount_form})
    
    def post(self, request, *args, **kwargs):
        add_amount_form = self.class_form(request.POST)
        if add_amount_form.is_valid():
            cd = add_amount_form.cleaned_data
            wallet = request.user.user_wallet
            TransectionRequest.objects.create(amount=cd['amount'], wallet=wallet)
            messages.warning(request, 'Please Wait admin to accept Your amount request', 'warning')            
            return redirect('wallet:wallet_balance')
        messages.error(request, 'Please Complete Form', 'danger')
        return render(request, 'wallet/add_amount_wallet_form.html', {'add_amount_form':add_amount_form})


class WalletBalanceListView(LoginRequiredMixin, View):
    def get(self, request):
        wallet_detail = request.user.user_wallet
        return render(request, 'wallet/wallet_balance_list.html', {'wallet_detail':wallet_detail})        


class TransectionRequestListView(IsAdmin, View):
    def get(self, request, transection_id):
        transection_request = TransectionRequest.objects.get(pk=transection_id)
        transection_request.is_accept = not transection_request.is_accept  
        transection_request.save()
        messages.success(request, 'Accepted.', 'success')
        return redirect('wallet:transection_list')

   
class TransecitonListView(IsAdmin, View):
    def get(self, request):
        param = request.GET.get('filter_by')
        if param == 'True':
            transection_list = TransectionRequest.objects.filter(is_accept=param).order_by('-created')
            return render(request, 'wallet/transection_temp/transection_list.html', {'transection_list':transection_list})
        elif param == 'False':
            transection_list = TransectionRequest.objects.filter(is_accept=param).order_by('-created')
            return render(request, 'wallet/transection_temp/transection_list.html', {'transection_list':transection_list})
        
        transection_list = TransectionRequest.objects.all().order_by('-created')
        return render(request, 'wallet/transection_temp/transection_list.html', {'transection_list':transection_list})


class TransectionLogListView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        get_transection = TransectionLog.objects.filter(wallet__user__id=user_id).order_by('-created')
        return render(request, 'wallet/transection_log/transection_log_list.html', {'get_transection':get_transection})
       
       
 
