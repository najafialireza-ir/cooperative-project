from django import forms
from management.models import City, DriverCar
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget


class TravelForm(forms.Form):
    driver_car = forms.ModelChoiceField(queryset=DriverCar.objects.all())
    startcity = forms.ModelChoiceField(queryset=City.objects.all())
    destanition = forms.ModelChoiceField(queryset=City.objects.all())
    time = forms.TimeField()
    date = JalaliDateField(widget=AdminJalaliDateWidget)


class TravelRegisterDriverForm(forms.Form):
    startcity = forms.ModelChoiceField(queryset=City.objects.all())
    destanition = forms.ModelChoiceField(queryset=City.objects.all())
    time = forms.TimeField()
    date = JalaliDateField(widget=AdminJalaliDateWidget)
