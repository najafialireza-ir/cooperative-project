from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Order, PurchasedOrder
from .forms import AddOrderForm
from accounts.models import User
from wallet.models import TransectionLog, Wallet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from travels.models import Travel, Ticket
from management.models import BasePercent

class TicketListUserView(View):
    form_class = AddOrderForm
    def get(self, request, *args, **kwargs):
        order_form = self.form_class
        base_percent = BasePercent.objects.all().last()
        tickets = Ticket.objects.filter(id=kwargs['ticket_id'])
        ticket = tickets.get(id=kwargs['ticket_id'])
        if ticket.is_available:
            return render(request, 'orders/ticket_details_user.html', {'order_form':order_form, 'tickets':tickets, 'base_percent':base_percent})
        messages.error(request, 'This Ticket not available!', 'danger')
        return redirect('travels:ticket_detail', ticket.travel.id)
    

class AddOrderView(LoginRequiredMixin, View):
    form_class = AddOrderForm

    def post(self, request, *args, **kwargs):
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
            add_cart.save() 
            ticket.user = user
            ticket.is_available = False
            ticket.save()
            return redirect('orders:cart_list', user.id)
        messages.error(request, 'You Must choice 1 item', 'danger')
        return redirect('orders:ticket_lsit_user', ticket.id)
        
       
class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, user_id, *args, **kwargs):
        orders = Order.objects.filter(user=user_id)
        wallet = Wallet.objects.get(user=user_id)
        
        for order in orders:
            product_price = order.get_cost
            check_credit = wallet.check_credit(product_price)
            if check_credit:
                wallet.withdraw(product_price)
                order.paid_price = product_price
                order.save()
                a = PurchasedOrder.objects.create(user_id=user_id, order=order)
                print(a)
                TransectionLog.objects.create(transection_type='2', wallet=wallet, 
                                            amount=(-product_price), log_ids=order.id)
                order.delete()
            else:
                messages.error(request, 'Your Account balance is Not insufficient!', 'danger')
                return redirect('wallet:add_amount')
        
        messages.success(request, 'Successfully paid', 'success')
        return redirect('orders:cart_list', order.user.id)
    

class CartListView(View):
    def get(self, request, user_id):
        orders = Order.objects.filter(user=user_id).order_by('-updated')
        last_item = orders.last()
        total_cost = (last_item.get_total_cost_for_user if last_item else 0)
        return render(request, 'orders/cart_list.html', {'orders':orders, 'total_cost':total_cost})


class PurchasedListView(LoginRequiredMixin, View):
    def get(self, request, user_id, *args, **kwargs):
        purchesd_list = PurchasedOrder.objects.filter(user_id=user_id)
        return render(request, 'orders/purchased_list.html', {'purchased':purchesd_list})


class PurchasedDeleteView(LoginRequiredMixin, View):
    def get(self, request):
        param = request.GET.get('purchase_id')
        if param:
            purchase = PurchasedOrder.objects.get(pk=param)
            purchase.delete()
            messages.success(request, 'Your purchase orders and money returned your wallet.', 'success')
            return redirect('orders:purchased_list', request.user.id)
        
 
class CartDeleteView(LoginRequiredMixin, View):
    def get(self, request):
        param = request.GET.get('order_id')
        if param:
            order = Order.objects.get(pk=param)
            order.delete()
            messages.success(request, 'Your order deleted.', 'success')
            return redirect('orders:cart_list', request.user.id)
        

