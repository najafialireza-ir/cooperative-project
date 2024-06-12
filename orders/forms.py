from django import forms
from django.core.exceptions import ValidationError

class AddOrderForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=1)
    
    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 1 or quantity > 1:
            raise ValidationError('your order must be 1 item')
        return quantity