from django import forms
from .models import City, Car
from accounts.models import User
from django.core.exceptions import ValidationError


class CityForm(forms.Form):
    city = forms.CharField(max_length=30)
    lat = forms.FloatField()
    lon = forms.FloatField()
    
    def clean_city(self):
        city = self.cleaned_data['city']
        city_model = City.objects.filter(name=city).exists()
        if city_model:
            raise ValidationError('This City Exists.', 'error')
        return city

        
class DriverRegisterForm(forms.Form):
    car = forms.ModelChoiceField(queryset=Car.objects.all())
    car_production_date = forms.DateField()
         

class CarRegisterForm(forms.Form):
    name = forms.CharField(max_length=20)
    capacity = forms.IntegerField(max_value=40) 
 
    
class CityChoiceForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('name',)
    
    
class DriverUser(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    

class BaseTimeForm(forms.Form):
    base_time = forms.IntegerField()
  
    
class BasePriceForm(forms.Form):
    price_per_km = forms.IntegerField()


class BasePercentForm(forms.Form):
    base_percent = forms.IntegerField()  


class BaseTimeRefundForm(forms.Form):
    base_time_refund = forms.IntegerField()