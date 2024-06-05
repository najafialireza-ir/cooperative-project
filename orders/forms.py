from django import forms
from .models import Order


class AddOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('quantity', )