from django.db import models
from accounts.models import Driver
from jalali_date import datetime2jalali, date2jalali


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
    
    @property
    def get_jalali_date(self):
        return date2jalali(self.car_production_date)
    

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
    
    @property
    def get_jalali_date(self):
        return datetime2jalali(self.created).replace(microsecond=0)
    
class BaseTime(models.Model):
    base_time = models.IntegerField()
 
    
class BasePercent(models.Model):
    base_percent = models.IntegerField()
    created = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.base_percent)
    
    @property
    def get_jalali_date(self):
        return date2jalali(self.created)
    
class BaseTimeRefund(models.Model):
    base_time = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now=True)
    
    @property
    def get_jalali_date(self):
        return datetime2jalali(self.created).replace(microsecond=0)