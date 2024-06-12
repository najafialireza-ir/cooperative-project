from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch import receiver
from .models import Order, PurchasedOrder
from management.models import BasePercent
from wallet.models import Wallet, TransectionLog
from travels.models import Ticket
from datetime import timedelta, datetime
from management.models import BaseTimeRefund


@receiver(pre_delete, sender=Order)
def return_paid_price(instance, sender, **kwargs):
    user = instance.user
    ticket = Ticket.objects.get(id=instance.ticket.id)
    ticket.is_available = True
    ticket.user = None
    ticket.save()
    paid_price = instance.paid_price
    try:
        if paid_price:
            wallet = Wallet.objects.get(user=user)
            percent = BasePercent.objects.all().last()
            deducted_amount = int((percent.base_percent / 100) * paid_price)
            result = paid_price - deducted_amount
            wallet.deposite(result)
            wallet.save()
            ticket.is_available = False
            ticket.user = instance.user
            ticket.save()
            TransectionLog.objects.create(transection_type='2', wallet=wallet, amount=paid_price, log_ids=instance.id)      
    except:
        pass 


@receiver(post_save, sender=PurchasedOrder)
def delete_order_create_purchased(instance, sender, created, **kwargs):
    if created:
        order = instance.order
        order.delete()
            

@receiver(pre_delete, sender=PurchasedOrder)
def return_ticket(instance, sender, **kwargs):
    ticket = Ticket.objects.get(id=instance.order.ticket.id)
    paid_price = instance.order.paid_price
    
    base_time_refund = BaseTimeRefund.objects.all().last()
    date_time_now = datetime.now()
    paid_date_time = instance.order.paid_date
    result = (date_time_now - paid_date_time)
    wallet = Wallet.objects.get(user=instance.user)
    
    try:
        if result > timedelta(seconds=base_time_refund.base_time):
            percent = BasePercent.objects.all().last()
            deducted_amount = int((percent.base_percent / 100) * paid_price)
            result = paid_price - deducted_amount
            wallet.deposite(result)
            wallet.save()  
            ticket.is_available = True
            ticket.user = None
            ticket.save()
    except:
        pass
    
    wallet.deposite(paid_price)
    wallet.save()  
    ticket.is_available = True
    ticket.user = None
    ticket.save()

