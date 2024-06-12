from django import forms
from .models import User
from management.models import Car, City
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
    car_production_date = forms.DateField()
         
    
class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    

class BaseTimeRefundForm(forms.Form):
    base_time_refund = forms.IntegerField()