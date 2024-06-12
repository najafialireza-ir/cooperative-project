from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from utils import IsAdmin
from .forms import (
    CityForm, 
    BasePriceForm, 
    BaseTimeForm, 
    CarRegisterForm, 
    DriverUser, 
    DriverRegisterForm, 
    BasePercentForm, 
    BaseTimeRefundForm,
)
from .models import City, DriverCar, Driver, Car, BaseTime, BasePrice, BasePercent, BaseTimeRefund
from travels.models import Travel
from django.contrib import messages


class AdminPanelView(View):
    def get(self, request):
        return render(request, 'management/admin_panel.html')
        
        
class ChangeCityView(IsAdmin, View):
    class_form = CityForm
    def get(self, request):
            city_form = self.class_form
            return render(request, 'management/admin_change_city.html', {'city_form':city_form})
      
    def post(self, request):
            city_form = self.class_form(request.POST)
            if city_form.is_valid():
                cd = city_form.cleaned_data
                City.objects.create(name=cd['city'], lat=cd['lat'], lon=cd['lon'])
                messages.success(request, 'City Submitted Successfully.')
                return redirect('management:list_city')
            return render(request, 'management/admin_change_city.html', {'city_form':city_form})

 
class ListCityView(IsAdmin, View):
    def get(self, request):
        cities = City.objects.all()
        return render(request, 'management/city_list.html', {'cities':cities})
        

class DriverRegisterAdminView(IsAdmin, View):
    driver_register_form = DriverRegisterForm
    user_select = DriverUser
    def get(self, request):
            form = self.driver_register_form
            user_select = self.user_select
            return render(request, 'management/admin_r_d.html', {'form':form, 'user_select':user_select})
    
    def post(self, request):
            form = self.driver_register_form(request.POST)
            user_select = self.user_select(request.POST)
            
            if form.is_valid() and user_select.is_valid():
                cd = form.cleaned_data
                driver = Driver.objects.create(user=user_select.cleaned_data['user'])
                messages.success(request, 'User Registered as a Driver.')
                DriverCar.objects.create(driver=driver, car=cd['car'], car_production_date=cd['car_production_date'])
                return redirect('management:driver_detail')
            return render(request, 'management/admin_r_d.html', {'form':form, 'user_select':user_select})
        
        
class DriverDetailView(IsAdmin, View):
    def get(self, request):
            drivers = DriverCar.objects.all()
            return render(request, 'management/driver_list.html', {'drivers':drivers})


class CarRegisterView(IsAdmin, View):
    class_form = CarRegisterForm
    def get(self, request):
        car_form = self.class_form
        return render(request, 'management/car_register.html', {'car_form':car_form})

    def post(self, request):
        car_form = self.class_form(request.POST)
        if car_form.is_valid():
            cd = car_form.cleaned_data
            Car.objects.create(name=cd['name'], capacity=cd['capacity'])
            messages.success(request, 'Car Registered.', 'success')
            return redirect('management:car_list')
        return render(request, 'management/car_register.html', {'car_form':car_form})


class CarListView(IsAdmin, View):
    def get(self, request):
        cars = Car.objects.all()
        return render(request, 'management/car_list.html', {'cars':cars})


class BasePriceList(IsAdmin, View):
    def get(self, request):
        prices = BasePrice.objects.all()
        return render(request, 'management/price_list.html', {'prices':prices})
    

class BasePriceView(IsAdmin, View):
    class_from = BasePriceForm
    def get(self, request):
        price_form = self.class_from
        return render(request, 'management/base_price.html', {'price_form':price_form})
    def post(self, request):
        price_form = self.class_from(request.POST)
        if price_form.is_valid():
            cd = price_form.cleaned_data
            BasePrice.objects.create(price_per_km=cd['price_per_km'])
            messages.success(request, 'baseprice created.', 'success')
            return redirect('management:price_list')
        return render(request, 'management/base_price.html', {'price_form':price_form})


class BaseTimeView(IsAdmin, View):
    form_class = BaseTimeForm
    def get(self, request):
        base_time_form = self.form_class
        return render(request, 'management/base_time_form.html', {'base_time_form':base_time_form})
    
    def post(self, request):
        base_time_form = self.form_class(request.POST)
        if base_time_form.is_valid():
            cd = base_time_form.cleaned_data
            BaseTime.objects.create(base_time=cd['base_time'])
            messages.success(request, 'basetime created.', 'success')
        return render(request, 'management/base_time_form.html', {'base_time_form':base_time_form})


class BasePercentView(IsAdmin, View):
    class_form = BasePercentForm
    def get(self, request):
        percent_form = self.class_form
        return render(request, 'management/base_percent_form.html', {'percent_form':percent_form})
    
    def post(self, request):
        percent_form = self.class_form(request.POST)
        if percent_form.is_valid():
            cd = percent_form.cleaned_data
            BasePercent.objects.create(base_percent=cd['base_percent'])
            messages.success(request, 'base percent successfully!', 'success')
            return redirect('management:admin_panel')
        return render(request, 'management/base_percent_form.html', {'percent_form':percent_form})
 
class BasePercentListView(IsAdmin, View):
    def get(self, request):
        percent_list = BasePercent.objects.all().order_by('-created')
        return render(request, 'management/base_percent_list.html', {'percent_list':percent_list})

        
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
            return redirect('management:list_city')
        
        
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
            return redirect('management:driver_detail')
     
        
class BaseTimeRefundView(IsAdmin, View):
    form_class = BaseTimeRefundForm
    def get(self, request):
        form = self.form_class
        return render(request, 'management/base_time_refund.html', {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            BaseTimeRefund.objects.create(base_time=cd['base_time_refund'])   
            messages.success(request, 'Base Time for deduction of refund.', 'success') 
            return redirect('management:base_time_refund_list')   
        messages.error(request, 'You must complete this form', 'danger')
        return render(request, 'management/base_time_refund.html', {'form':form})
   
    
class BaseTimeRefundList(IsAdmin, View):
    def get(self, request):
        time_refund = BaseTimeRefund.objects.all().order_by('-created')
        return render(request, 'management/base_time_refund_list.html', {'time_refund':time_refund})