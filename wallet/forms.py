from django import forms


class AddAmountWalletForm(forms.Form):
    amount = forms.IntegerField()
    
    
