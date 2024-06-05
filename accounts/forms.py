from django import forms
from .models import User, City, Car, Travel, DriverCar
from django.core.exceptions import ValidationError


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('email', 'user_type', 'username')
        
        
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email exists!')
        return email
        
         
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('password doesn`t match')
        return cd['password2']
    
 
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user
    
        
class DriverRegisterForm(forms.Form):
    car = forms.ModelChoiceField(queryset=Car.objects.all())
    city = forms.ModelChoiceField(queryset=City.objects.all())
    production_date = forms.DateField()
     
    
class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    

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
    

class CarRegisterForm(forms.Form):
    name = forms.CharField(max_length=20)
    capacity = forms.IntegerField(max_value=40) 
 
    
class CityChoiceForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('name',)
    
    
class DriverUser(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    
    
class TravelForm(forms.Form):
    driver_car = forms.ModelChoiceField(queryset=DriverCar.objects.all())
    startcity = forms.ModelChoiceField(queryset=City.objects.all())
    destanition = forms.ModelChoiceField(queryset=City.objects.all())
  
    date_time = forms.DateTimeField()
    
   
class TravelRegisterDriverForm(forms.Form):
    startcity = forms.ModelChoiceField(queryset=City.objects.all())
    destanition = forms.ModelChoiceField(queryset=City.objects.all())
    date_time = forms.DateTimeField()

class BaseTimeForm(forms.Form):
    base_time = forms.IntegerField()
    
class BasePriceForm(forms.Form):
    price_per_km = forms.IntegerField()
    

class AddAmountWalletForm(forms.Form):
    amount = forms.IntegerField()
    
    
class BasePercentForm(forms.Form):
    base_percent = forms.IntegerField()