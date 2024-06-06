from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import (
    UserRegisterForm, 
    DriverRegisterForm, 
    UserLoginForm, 
    CityForm,
    DriverUser, 
    TravelForm, 
    TravelRegisterDriverForm,
    BaseTimeForm,
    BasePriceForm,
    CarRegisterForm,
    AddAmountWalletForm,
    BasePercentForm,
    )
from .models import (
    User, Driver, 
    DriverCar, City, 
    Travel, Car, 
    BasePrice, BaseTime,
    Wallet, TransectionRequest,
    TransectionLog,
    BasePercent,
    )
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from utils import IsAdmin


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
        user = get_object_or_404(User, pk=user_id)
        form = self.form_class(request.POST)
        if user.user_type == '2':

            if form.is_valid():
                cd = form.cleaned_data
                driver = Driver.objects.create(user=user, city=cd['city'])
                messages.success(request, 'You Registered as a Driver.')
                DriverCar.objects.create(driver=driver, car=cd['car'], production_date=cd['production_date'])
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
                return render(request, 'accounts/login.html', {'form':form})
            login(request, user)
            
            if user.user_type == '1': # user
                messages.success(request, 'You logged in')
                return redirect('home:home')
            
            elif user.user_type == '2': # driver
                messages.success(request, 'You logged in')
                return redirect('accounts:driver_travel', user.id)
            
            elif user.user_type == '3' and user.is_superuser:
                messages.success(request, 'You logged in as Admin')
                return redirect('accounts:admin_panel')
        return render(request, 'accounts/user/login.html', {'form':form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You Logouted')
        return redirect('home:home')
    
    
class AdminPanelView(View):
    def get(self, request):
        return render(request, 'accounts/admin_panel.html')
        
        
class ChangeCityView(IsAdmin, View):
    class_form = CityForm
    def get(self, request):
            city_form = self.class_form
            return render(request, 'accounts/admin_change_city.html', {'city_form':city_form})
      
    def post(self, request):
            city_form = self.class_form(request.POST)
            if city_form.is_valid():
                cd = city_form.cleaned_data
                City.objects.create(name=cd['city'], lat=cd['lat'], lon=cd['lon'])
                messages.success(request, 'City Submitted Successfully.')
                return redirect('accounts:list_city')
            return render(request, 'accounts/admin_change_city.html', {'city_form':city_form})
        
    
class ListCityView(IsAdmin, View):
    def get(self, request):
        cities = City.objects.all()
        return render(request, 'accounts/city_list.html', {'cities':cities})
        

class DriverRegisterAdminView(IsAdmin, View):
    driver_register_form = DriverRegisterForm
    user_select = DriverUser
    def get(self, request):
            form = self.driver_register_form
            user_select = self.user_select
            return render(request, 'accounts/admin_r_d.html', {'form':form, 'user_select':user_select})
    
    def post(self, request):
            form = self.driver_register_form(request.POST)
            user_select = self.user_select(request.POST)
            
            if form.is_valid() and user_select.is_valid():
                cd = form.cleaned_data
                driver = Driver.objects.create(user=user_select.cleaned_data['user'], city=cd['city'])
                messages.success(request, 'User Registered as a Driver.')
                DriverCar.objects.create(driver=driver, car=cd['car'], production_date=cd['production_date'])
                return redirect('accounts:driver_detail')
            return render(request, 'accounts/admin_r_d.html', {'form':form, 'user_select':user_select})
        
        
class DriverDetailView(IsAdmin, View):
    def get(self, request):
            drivers = DriverCar.objects.all()
            return render(request, 'accounts/driver/driver_list.html', {'drivers':drivers})
 

class DriverProfileView(View):
    def get(self, request, driver_id):
        if request.user.is_authenticated and request.user.user_type == '2':
            drivers = DriverCar.objects.filter(driver__user=driver_id)
            return render(request, 'accounts/driver/driver_profile.html', {'drivers': drivers})  
        
        
class TravelDriverInfo(View):
    def get(self, request, user_id):
        if request.user.is_authenticated and request.user.user_type == '2':
            travels =  Travel.objects.filter(driver_car__driver__user=user_id)
            return render(request, 'accounts/driver/driver_travel_info.html', {'travels':travels})
 

class DriverRegisterTravel(LoginRequiredMixin, View):
    travel_form = TravelRegisterDriverForm
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == '2':
            travel_form = self.travel_form
            return render(request, 'accounts/driver/driver_register_travel.html', {'travel_form':travel_form})
                 
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == '2':
            travel_form = self.travel_form(request.POST)
            if travel_form.is_valid():
                cd = travel_form.cleaned_data
                user = get_object_or_404(DriverCar, id=request.user.id)
        
                travel = Travel(driver_car=user, startcity=cd['startcity'],
                                      destanition=cd['destanition'], date_time=cd['date_time'])
                travel.end_time = travel.get_time
                travel.price = travel.get_cost
                is_travel_exists = Travel.objects.filter(driver_car=travel.driver_car, 
                                                         date_time__range=[travel.date_time, travel.end_time ]).exists()
                if is_travel_exists:
                    messages.error(request, 'driver this time is on travel.', 'danger')
                    return render(request, 'accounts/raise_error_trip_driver.html', {'travel':travel})
                travel.save()
                messages.success(request, 'Please Wait admin to accept Your`s travel', 'warning')
                return redirect('accounts:driver_travel', user.id)
        messages.error(request, 'You don`t access this page.', 'danger')
                

class ApproveTravelAdminView(IsAdmin, View):
    def get(self, request, travel_id):
        travel = get_object_or_404(Travel, id=travel_id)
        travel.approved = True
        travel.save()
        messages.success(request, 'Travel Approved and ticket submitted.', 'success')
        return redirect('accounts:travel_detail')
    
                    
class TravelRegisterView(IsAdmin, View):
    travel_form_class = TravelForm
    def get(self, request):
            travel_form = self.travel_form_class
            return render(request, 'accounts/travel_admin.html', {'travel_form':travel_form})

    def post(self, request):
        if request.user.user_type == '3' and request.user.is_superuser:
            travel_form = self.travel_form_class(request.POST)
        
            if travel_form.is_valid():
                cd = travel_form.cleaned_data
                travel = Travel(driver_car=cd['driver_car'], startcity=cd['startcity'],
                                      destanition=cd['destanition'], date_time=cd['date_time'])
                travel.end_time = travel.get_time
                travel.price = travel.get_cost
                is_travel_exists = Travel.objects.filter(driver_car=travel.driver_car, 
                                                         date_time__range=[travel.date_time, travel.end_time ]).exists()
                
                if is_travel_exists:
                    messages.error(request, 'driver this time is on travel.', 'danger')
                    return render(request, 'accounts/raise_error_trip_driver.html', {'travel':travel})
                travel.approved = True
                travel.save()
                messages.success(request, 'New Travel And Ticket Created', 'success')
                return redirect('accounts:travel_detail')
            return render(request, 'accounts/travel_admin.html', {'travel_form':travel_form})
        messages.error(request, 'You can`t access this page', 'danger')
        
        
class TravelListView(IsAdmin, View):
    def get(self, request):
        travels = Travel.objects.all()
        return render(request, 'accounts/travel_list.html', {'travels':travels})


class CarRegisterView(IsAdmin, View):
    class_form = CarRegisterForm
    def get(self, request):
        car_form = self.class_form
        return render(request, 'accounts/car_register.html', {'car_form':car_form})

    def post(self, request):
        car_form = self.class_form(request.POST)
        if car_form.is_valid():
            cd = car_form.cleaned_data
            Car.objects.create(name=cd['name'], capacity=cd['capacity'])
            messages.success(request, 'Car Registered.', 'success')
            return redirect('accounts:car_list')
        return render(request, 'accounts/car_register.html', {'car_form':car_form})


class CarListView(IsAdmin, View):
    def get(self, request):
        cars = Car.objects.all()
        return render(request, 'accounts/car_list.html', {'cars':cars})


class BasePriceList(IsAdmin, View):
    def get(self, request):
        prices = BasePrice.objects.all()
        return render(request, 'accounts/price_list.html', {'prices':prices})
    

class BasePriceView(IsAdmin, View):
    class_from = BasePriceForm
    def get(self, request):
        price_form = self.class_from
        return render(request, 'accounts/base_price.html', {'price_form':price_form})
    def post(self, request):
        price_form = self.class_from(request.POST)
        if price_form.is_valid():
            cd = price_form.cleaned_data
            BasePrice.objects.create(price_per_km=cd['price_per_km'])
            messages.success(request, 'baseprice created.', 'success')
            return redirect('accounts:price_list')
        return render(request, 'accounts/base_price.html', {'price_form':price_form})


class BaseTimeView(IsAdmin, View):
    form_class = BaseTimeForm
    def get(self, request):
        base_time_form = self.form_class
        return render(request, 'accounts/base_time_form.html', {'base_time_form':base_time_form})
    
    def post(self, request):
        base_time_form = self.form_class(request.POST)
        if base_time_form.is_valid():
            cd = base_time_form.cleaned_data
            BaseTime.objects.create(base_time=cd['base_time'])
            messages.success(request, 'basetime created.', 'success')
        return render(request, 'accounts/base_time_form.html', {'base_time_form':base_time_form})
  

class AddAmountWalletView(LoginRequiredMixin, View):
    class_form = AddAmountWalletForm
    def get(self, request, *args, **kwargs):
        add_amount_form = self.class_form
        return render(request, 'accounts/add_amount_wallet_form.html', {'add_amount_form':add_amount_form})
    
    def post(self, request, *args, **kwargs):
        add_amount_form = self.class_form(request.POST)
        if add_amount_form.is_valid():
            cd = add_amount_form.cleaned_data
            wallet = request.user.user_wallet
            TransectionRequest.objects.create(amount=cd['amount'], wallet=wallet)
            messages.warning(request, 'Please Wait admin to accept Your amount request', 'warning')            
            return redirect('accounts:wallet_balance')
        messages.error(request, 'Please Complete Form', 'danger')
        return render(request, 'accounts/add_amount_wallet_form.html', {'add_amount_form':add_amount_form})


class WalletBalanceListView(LoginRequiredMixin, View):
    def get(self, request):
        wallet_detail = request.user.user_wallet
        return render(request, 'accounts/wallet_balance_list.html', {'wallet_detail':wallet_detail})        


class TransectionRequestListView(IsAdmin, View):
    def get(self, request, transection_id):
        transection_request = TransectionRequest.objects.get(pk=transection_id)
        transection_request.is_accept = not transection_request.is_accept  
        transection_request.save()
        messages.success(request, 'Accepted.', 'success')
        return redirect('accounts:transection_list')

   
class TransecitonListView(IsAdmin, View):
    def get(self, request):
        param = request.GET.get('filter_by')
        if param == 'True':
            transection_list = TransectionRequest.objects.filter(is_accept=param).order_by('-created')
            return render(request, 'accounts/transection_temp/transection_list.html', {'transection_list':transection_list})
        elif param == 'False':
            transection_list = TransectionRequest.objects.filter(is_accept=param).order_by('-created')
            return render(request, 'accounts/transection_temp/transection_list.html', {'transection_list':transection_list})
        
        transection_list = TransectionRequest.objects.all().order_by('-created')
        return render(request, 'accounts/transection_temp/transection_list.html', {'transection_list':transection_list})


class TransectionLogListView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        try:
            get_transection = TransectionLog.objects.filter(wallet__user__id=user_id).order_by('-created')
            return render(request, 'accounts/transection_log/transection_log_list.html', {'get_transection':get_transection})
        except:
            pass
 
 
class BasePercentView(IsAdmin, View):
    class_form = BasePercentForm
    def get(self, request):
        percent_form = self.class_form
        return render(request, 'accounts/base_percent_form.html', {'percent_form':percent_form})
    
    def post(self, request):
        percent_form = self.class_form(request.POST)
        if percent_form.is_valid():
            cd = percent_form.cleaned_data
            BasePercent.objects.create(base_percent=cd['base_percent'])
            messages.success(request, 'base percent successfully!', 'success')
            return redirect('accounts:admin_panel')
        return render(request, 'accounts/base_percent_form.html', {'percent_form':percent_form})
 
 
class DeleteTravelView(IsAdmin, View):                
    def get(self, request):
        travel_ids = request.GET.get('travel_id')
        
        try:
            travel_ids = travel_ids.split(",")
        except:
            travel_ids = []
        if travel_ids:
            Travel.objects.filter(id__in=travel_ids).delete()
            messages.success(request, 'Travel deleted')
            return redirect('accounts:travel_detail')
        
            
class DeleteCityView(IsAdmin, View):
    def get(self, request):
        city_ids = request.GET.get('city_ids')
        try:
            city_ids = city_ids.split(",")
        except:
            city_ids = []
        if city_ids:
            City.objects.filter(id__in=city_ids).delete()
            messages.success(request, 'City deleted')
            return redirect('accounts:list_city')
        
        
class DeleteDriverView(IsAdmin, View):
    def get(self, request):
        driver_ids = request.GET.get('driver_id')
        try:
            driver_ids = driver_ids.split(',')
        except:
            driver_ids = []
        if driver_ids:
            Driver.objects.filter(id__in=driver_ids).delete()
            messages.success(request, 'Driver deleted')
            return redirect('accounts:driver_detail')
        
