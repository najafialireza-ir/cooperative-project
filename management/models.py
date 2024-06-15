from django.db import models
from accounts.models import Driver


class Car(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()
   
    def __str__(self):
       return f'{self.name}'
   
    
class DriverCar(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    car_production_date = models.DateField()
    
    def __str__(self):
        return f'{self.driver}-{self.car}'


class City(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lon = models.FloatField()

    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.name
    

class BasePrice(models.Model):
    price_per_km = models.IntegerField()
    created = models.DateTimeField(auto_now=True)
    
class BaseTime(models.Model):
    base_time = models.IntegerField()
 
    
class BasePercent(models.Model):
    base_percent = models.IntegerField()
    created = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.base_percent)
    
class BaseTimeRefund(models.Model):
    base_time = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now=True)