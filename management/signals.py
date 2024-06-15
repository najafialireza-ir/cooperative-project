from django.db.models.signals import post_save
from django.dispatch import receiver
from travels.models import Travel, Ticket
from .models import BasePrice
from orders.models import Order

@receiver(post_save, sender=BasePrice)
def update_travel_prices(sender, instance, created, **kwargs):
    if created:
        new_price = instance.price_per_km
        travel_ids_tickets = Ticket.objects.filter(is_available=True, user__isnull=True).values_list('travel_id', flat=True).distinct()
        travels = Travel.objects.filter(id__in=travel_ids_tickets)
        for travel in travels:
            travel.price = new_price * travel.get_distance
            travel.save()