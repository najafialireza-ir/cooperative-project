from django.db import models
from accounts.models import User, Travel


class Ticket(models.Model):
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, related_name='travel_ticket')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_ticket')
    is_available = models.BooleanField(default=True)

    @property
    def get_capacity(self):
        users_count = Order.objects.get(ticket__travel=self.travel)
        ticket_capacity = self.travel.driver_car.car.capacity - users_count.quantity
        return ticket_capacity
  
  
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_user')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    paid_price = models.IntegerField(null=True)
    paid_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    @property
    def get_cost(self):
        return self.ticket.travel.price * self.quantity

    @property
    def get_total_cost_for_user(self):
        orders = Order.objects.filter(user=self.user)
        total_cost = sum(order.get_cost for order in orders)
        return total_cost