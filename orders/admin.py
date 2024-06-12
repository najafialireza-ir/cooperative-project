from django.contrib import admin
from .models import Ticket, Order, PurchasedOrder


admin.site.register(Ticket)
admin.site.register(Order)
admin.site.register(PurchasedOrder)


