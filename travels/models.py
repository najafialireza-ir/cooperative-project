from django.db import models
import haversine as hs
from haversine import Unit
from datetime import timedelta
from management.models import DriverCar, City, BasePrice, BaseTime
from accounts.models import User


class Travel(models.Model):
    driver_car = models.ForeignKey(DriverCar, on_delete=models.CASCADE, related_name='driver_car')
    startcity = models.ForeignKey(City, on_delete=models.CASCADE, related_name='s_travel')
    destanition = models.ForeignKey(City, on_delete=models.CASCADE, related_name='d_travel')
    price = models.IntegerField(null=True, blank=True)
    date_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(default=False) 
    quantity = models.IntegerField(null=True)
    
    def __str__(self):
        return f'{self.startcity}-{self.destanition}-({self.date_time})'

    @property
    def get_distance(self):
        city_1 = self.startcity
        city_2 = self.destanition
        if not (city_1 or city_2):
            return 0
        loc1 = (city_1.lat, city_1.lon)
        loc2 = (city_2.lat, city_2.lon)
        result = hs.haversine(loc1,loc2, unit=Unit.KILOMETERS)
        return int(result)
    
    @property
    def get_cost(self):
        base_price = BasePrice.objects.all().last()
        return base_price.price_per_km * self.get_distance
    
    @property
    def get_time(self):
        base_t = BaseTime.objects.all().last()
        time = base_t.base_time * self.get_distance
        time_remain = self.date_time + timedelta(seconds=time)
        return time_remain
    
    @property
    def get_capacity(self):
        user = Ticket.objects.filter(travel=self, user__isnull=False).count()
        count_quantity = self.quantity - user
        return count_quantity
    
    
class Ticket(models.Model):
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, related_name='travel_ticket')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_ticket')
    is_available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)
    seat_number = models.PositiveIntegerField(null=True)
    
    def __str__(self) -> str:
        return f'{self.travel}'
    
    