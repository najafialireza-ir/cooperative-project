from django.db import models
from accounts.models import User
from django.contrib.auth import get_user_model
from travels.models import Ticket
from .manager import SoftDeleteManager
from django.db.models.signals import pre_delete
from jalali_date import datetime2jalali


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_user')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    paid_price = models.IntegerField(null=True)
    paid_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False ,null=True, blank=True)
    
    # first objects - filters applied to object
    # second - all models without filter 
    objects = SoftDeleteManager()  # Custom manager for non-deleted objects
    all_objects = models.Manager()  # Default manager to access all objects, including soft-deleted ones
    
    def __str__(self) -> str:
        return f'{self.ticket.travel}'
 
    def delete(self):
        pre_delete.send(sender=self.__class__, instance=self)
        self.is_deleted = True
        self.save()
        
    @property
    def get_cost(self):
        return self.ticket.travel.price * self.quantity


    @property
    def get_total_cost_for_user(self):
        orders = Order.objects.filter(user=self.user)
        total_cost = sum(order.get_cost for order in orders)
        return total_cost
    
    @property
    def get_jalali_date(self):
        return datetime2jalali(self.created).replace(microsecond=0)
    
    
class PurchasedOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchased_user')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='purchased_order')
    created = models.DateTimeField(auto_now=True)
    
    @property
    def get_jalali_date(self):
        return datetime2jalali(self.created).replace(microsecond=0)