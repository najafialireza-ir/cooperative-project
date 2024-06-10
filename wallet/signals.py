from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.models import User
from .models import TransectionLog, TransectionRequest


@receiver(pre_save, sender=TransectionRequest)
def update_wallet_balance(sender, instance, raw, **kwargs):
    try:
        old_instance = TransectionRequest.objects.get(id=instance.id)
        wallet = instance.wallet
        
        if instance.is_accept and not old_instance.is_accept:
            wallet.deposite(instance.amount)  
            TransectionLog.objects.create(transection_type='1', wallet=instance.wallet, amount=instance.amount, log_ids=instance.id)      
        elif not instance.is_accept and  old_instance.is_accept:
            wallet.withdraw(instance.amount)  
            TransectionLog.objects.create(transection_type='1', wallet=instance.wallet, amount=(-instance.amount), log_ids=instance.id)      
        wallet.save()
    except:
        pass
    

