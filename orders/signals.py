from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from .models import Order
from accounts.models import Wallet, BasePercent


@receiver(pre_delete, sender=Order)
def return_paid_price(instance, sender, **kwargs):
    user = instance.user
    paid_price = instance.paid_price
    if paid_price:
        wallet = Wallet.objects.get(user=user)
        percent = BasePercent.objects.all().last()
        deducted_amount = int((percent.base_percent / 100) * paid_price)
        result = paid_price - deducted_amount
        wallet.deposite(result)
        wallet.save()
        

  