from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegisterForm, DriverRegisterForm, UserLoginForm 
from .models import  User, Driver
from management.models import DriverCar
from travels.models import Travel
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin


class UserRegisterView(View):
    form_class = UserRegisterForm
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/user/register.html', {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            user_type = form.cleaned_data['user_type']
            print(user_type)
            
            if user_type == '1': # user
                User.objects.create_user(email=cd['email'],password=cd['password2'],
                                         username=cd['username'], user_type=cd['user_type'])
                
                messages.success(request, 'You Registered as a User!')
                return redirect('home:home')
            
            elif user_type == '2' : # driver
                user = User.objects.create_driver(email=cd['email'], password=cd['password2'],
                                         username=cd['username'],
                                         user_type=cd['user_type'])
                messages.warning(request, 'You Must Complete This Form For a Driver', 'warning')
                return redirect('accounts:driver_register', user.id)
            
            elif user_type == '3': # admin
                User.objects.create_superuser(email=cd['email'], password=cd['password2'],
                                         username=cd['username'], user_type=cd['user_type'])
                
                messages.success(request, 'You Registered as a SuperUser!')
                return redirect('home:home')
            
        else:
            messages.error(request, 'You Must Complete Form!', 'danger')
            return render(request, 'accounts/user/register.html', {'form':self.form_class})
    
    
class DriverRegisterView(View):
    form_class = DriverRegisterForm
    
    def get(self, request, *args, **kwargs):
            form = self.form_class
            return render(request, 'accounts/driver/driver.html', {'form':form})
        
    def post(self, request, user_id, *args, **kwargs):
        user = User.objects.get(pk=user_id)
        
        form = self.form_class(request.POST)
        if user.user_type == '2':

            if form.is_valid():
                cd = form.cleaned_data
                driver = Driver.objects.create(user=user)
                DriverCar.objects.create(driver=driver, car=cd['car'], car_production_date=cd['car_production_date'])
                messages.success(request, 'You Registered as a Driver.')
                return redirect('home:home')
        return render(request, 'accounts/driver/driver.html', {'form':form})
    

class UserLoginView(View):
    form_class = UserLoginForm
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/user/login.html', {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if not user:
                messages.error(request, 'UserName Password is Wrong!', 'danger')
                return render(request, 'accounts/user/login.html', {'form':form})
            login(request, user)
            
            if user.user_type == '1': # user
                messages.success(request, 'You logged in')
                return redirect('home:home')
            
            elif user.user_type == '2': # driver
                messages.success(request, 'You logged in')
                return redirect('accounts:driver_travel', user.id)
            
            elif user.user_type == '3' and user.is_superuser:
                messages.success(request, 'You logged in as Admin')
                return redirect('management:admin_panel')
        return render(request, 'accounts/user/login.html', {'form':form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You Logouted')
        return redirect('home:home')
    
   
class DriverProfileView(LoginRequiredMixin, View):
    def get(self, request, driver_id):
        if request.user.user_type == '2':
            drivers = DriverCar.objects.filter(driver__user=driver_id)
            return render(request, 'accounts/driver/driver_profile.html', {'drivers': drivers})  
        
        
class TravelDriverInfo(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.user_type == '2':
            travels =  Travel.objects.filter(driver_car__driver__user=request.user).order_by('-date_time')
            return render(request, 'accounts/driver/driver_travel_info.html', {'travels':travels})
 

