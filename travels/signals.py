from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Travel, Ticket
from orders.models import Order


@receiver(post_save, sender=Travel)
def create_ticket(sender, instance, created, **kwargs):
    if instance.approved:
        for _ in range(instance.quantity):
            Ticket.objects.create(travel=instance)
        
