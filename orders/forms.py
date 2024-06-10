from django import forms

class AddOrderForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)