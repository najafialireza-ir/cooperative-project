from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Travel, User, Wallet, TransectionRequest, TransectionLog
from orders.models import Ticket


@receiver(post_save, sender=Travel)
def create_ticket(sender, instance, created, **kwargs):
    if instance.approved:
        Ticket.objects.create(travel=instance)
        

@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)
        

@receiver(pre_save, sender=TransectionRequest)
def update_wallet_balance(sender, instance, raw, **kwargs):
    try:
        old_instance = TransectionRequest.objects.get(id=instance.id)
        wallet = instance.wallet
        
        if instance.is_accept and not old_instance.is_accept:
            wallet.deposite(instance.amount)  
        elif not instance.is_accept and  old_instance.is_accept:
            wallet.withdraw(instance.amount)   
        wallet.save()
        TransectionLog.objects.create(transection_type='1', wallet=instance.wallet, amount=instance.amount)      
    except:
        pass
    

