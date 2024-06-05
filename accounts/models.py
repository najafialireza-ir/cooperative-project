from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
import haversine as hs
from haversine import Unit
from datetime import timedelta, datetime


class User(AbstractUser):
    email = models.EmailField(max_length=250, unique=True)
    choice = (('1', 'user'),('2', 'driver'),('3', 'admin'))
    user_type = models.CharField(max_length=10, choices=choice)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type', 'username']
 
    
    def __str__(self):
        return f'{self.email}'
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
 

class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver')
    city = models.ForeignKey('accounts.City', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username


class Car(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()
    
    def __str__(self):
       return f'{self.name}'
   
   
    
class DriverCar(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    production_date = models.DateField()
    
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
    

class Travel(models.Model):
    driver_car = models.ForeignKey(DriverCar, on_delete=models.CASCADE, related_name='driver_car')
    startcity = models.ForeignKey(City, on_delete=models.CASCADE, related_name='s_travel')
    destanition = models.ForeignKey(City, on_delete=models.CASCADE, related_name='d_travel')
    price = models.IntegerField(null=True, blank=True)
    date_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(default=False) 
    
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
    
        

class BasePrice(models.Model):
    price_per_km = models.IntegerField()
    date_time = models.DateTimeField(auto_now=True)
    
class BaseTime(models.Model):
    base_time = models.IntegerField()
 
    
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_wallet')
    balance = models.IntegerField(default=0)  
 
    def deposite(self, amount):
        self.balance += amount
        self.save()
         
    def check_credit(self, amount):
        return amount <= self.balance
   
    def withdraw(self, amount):
        self.balance -= amount
        self.save()

  
class TransectionRequest(models.Model):
    """request for addtion wallet"""
    is_accept = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.IntegerField() 
    
    
class TransectionLog(models.Model):
    """ bill """
    choice = (('1', 'request'),('2', 'order'))
    transection_type = models.CharField(max_length=10, choices=choice, null=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    

class BasePercent(models.Model):
    base_percent = models.IntegerField()