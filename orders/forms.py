from django import forms
from .models import Order


class AddOrderForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)