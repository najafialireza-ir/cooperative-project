from django import forms
from management.models import City, DriverCar


class TravelForm(forms.Form):
    driver_car = forms.ModelChoiceField(queryset=DriverCar.objects.all())
    startcity = forms.ModelChoiceField(queryset=City.objects.all())
    destanition = forms.ModelChoiceField(queryset=City.objects.all())
    date_time = forms.DateTimeField()


class TravelRegisterDriverForm(forms.Form):
    startcity = forms.ModelChoiceField(queryset=City.objects.all())
    destanition = forms.ModelChoiceField(queryset=City.objects.all())
    date_time = forms.DateTimeField()