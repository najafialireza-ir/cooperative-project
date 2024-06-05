from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Ticket, Order
from .forms import AddOrderForm
from accounts.models import User, TransectionLog
from utils import IsAdmin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from accounts.models import Wallet


class TicketListAdminView(IsAdmin, View):
    def get(self, request, *args, **kwargs):
        if request.user.user_type == '3':
            tickets = Ticket.objects.all()
            return render(request, 'orders/ticket_list.html', {'tickets':tickets})
        

class TicketDetailUserView(View):
    """ ticket detail show for normal user"""   
    form_class = AddOrderForm
    def get(self, request, *args, **kwargs):
        order_form = self.form_class
        tickets = Ticket.objects.filter(pk=kwargs['ticket_id'])
        return render(request, 'orders/ticket_details.html', {'order_form':order_form, 'tickets':tickets})
    
    
class AddOrderView(LoginRequiredMixin, View):
    form_class = AddOrderForm

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            order_form = self.form_class(request.POST)
            user = get_object_or_404(User, pk=request.user.id)
            ticket =  get_object_or_404(Ticket, pk=kwargs['ticket_id'])
            if order_form.is_valid():
                add_cart, crt = Order.objects.get_or_create(user=user, ticket=ticket)
                add_cart.user = user
                add_cart.ticket = ticket
                add_cart.quantity += order_form.cleaned_data['quantity']
                wallet = Wallet.objects.get(user=user)
                product_price = ticket.travel.price
                check_credit = wallet.check_credit(product_price)
                if check_credit:
                    wallet.withdraw(product_price)
                    add_cart.paid_price = product_price
                    add_cart.save()
                    TransectionLog.objects.create(transection_type='2', wallet=wallet, amount=product_price)
                    return redirect('orders:orders_detail', user.id)
                else:
                    messages.error(request, 'Your Account balance is Not insufficient!', 'danger')
                    return redirect('accounts:add_amount')
        messages.error(request, 'You must login in web site', 'danger') 
      
       
class OrderDetailView(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        orders = Order.objects.filter(user=user).order_by('-updated')
        return render(request, 'orders/orders_detail.html', {'orders':orders})
    
     
class OrderDeleteView(LoginRequiredMixin, View):
    def get(self, request):
        param = request.GET.get('order_id')
        if param:
            order = Order.objects.get(pk=param)
            order.delete()
            messages.success(request, 'Your order deleted and money returned your wallet.', 'success')
            return redirect('orders:orders_detail', request.user.id)
        

