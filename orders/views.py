from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Order
from .forms import AddOrderForm
from accounts.models import User
from wallet.models import TransectionLog, Wallet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from travels.models import Travel, Ticket


class TicketListUserView(View):
    form_class = AddOrderForm
    def get(self, request, *args, **kwargs):
        order_form = self.form_class
        tickets = Ticket.objects.filter(id=kwargs['ticket_id'])
        ticket = tickets.get(id=kwargs['ticket_id'])
        if ticket.is_available:
            return render(request, 'orders/ticket_details_user.html', {'order_form':order_form, 'tickets':tickets})
        messages.error(request, 'This Ticket not available!', 'danger')
        return redirect('travels:ticket_detail', ticket.travel.id)
    

class AddOrderView(LoginRequiredMixin, View):
    form_class = AddOrderForm

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            order_form = self.form_class(request.POST)
            user = get_object_or_404(User, pk=request.user.id)
            ticket = Ticket.objects.get(id=kwargs['travel_id'])
            if order_form.is_valid():
                cd = order_form.cleaned_data
                if cd['quantity'] > ticket.travel.quantity:
                    messages.error(request, 'Your request greater than of quantity!', 'danger')
                    return redirect('home:home')
                
                add_cart, crt = Order.objects.get_or_create(user=user, ticket=ticket)
                add_cart.ticket = ticket
                add_cart.quantity += cd['quantity']
                wallet = Wallet.objects.get(user=user)
                product_price = ticket.travel.price
                check_credit = wallet.check_credit(product_price)
                
                if check_credit:
                    wallet.withdraw(product_price)
                    add_cart.paid_price = product_price
                    add_cart.save()
                    TransectionLog.objects.create(transection_type='2', wallet=wallet, amount=(-product_price), log_ids=add_cart.id)
                    ticket.user = user
                    ticket.is_available = False
                    ticket.save()
                    return redirect('orders:orders_detail', user.id)
                else:
                    messages.error(request, 'Your Account balance is Not insufficient!', 'danger')
                    return redirect('wallet:add_amount')
            messages.error(request, 'You Must choice 1 item', 'danger')
        
        messages.error(request, 'You must login in web site', 'danger') 

class OrderPayView(LoginRequiredMixin, View):
    def get(self, request):
        pass

       
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
        

