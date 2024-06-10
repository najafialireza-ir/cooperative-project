from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from management.models import DriverCar
from travels.models import Travel, Ticket
from django.contrib import messages
from utils import IsAdmin
from .forms import TravelForm, TravelRegisterDriverForm

 
class DriverRegisterTravel(LoginRequiredMixin, View):
    travel_form = TravelRegisterDriverForm
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == '2':
            travel_form = self.travel_form
            return render(request, 'travels/driver_register_travel.html', {'travel_form':travel_form})
                 
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == '2':
            travel_form = self.travel_form(request.POST)
            if travel_form.is_valid():
                cd = travel_form.cleaned_data
                # user = get_object_or_404(DriverCar, driver_id=kwargs['driver_id'])
            
                user = DriverCar.objects.get(driver_id=kwargs['user_id'])
                travel = Travel(driver_car=user, startcity=cd['startcity'],
                                      destanition=cd['destanition'], date_time=cd['date_time'])
                travel.end_time = travel.get_time
                travel.price = travel.get_cost
                travel.quantity = travel.driver_car.car.capacity
                is_travel_exists = Travel.objects.filter(driver_car=travel.driver_car, 
                                                         date_time__range=[travel.date_time, travel.end_time ]).exists()
                if is_travel_exists:
                    messages.error(request, 'driver this time is on travel.', 'danger')
                    return render(request, 'travels/raise_error_trip_driver.html', {'travel':travel})
                travel.save()
                messages.success(request, 'Please Wait admin to accept Your`s travel', 'warning')
                return redirect('accounts:driver_travel', user.id)
        messages.error(request, 'You don`t access this page.', 'danger')


class TravelListView(IsAdmin, View):
    def get(self, request):
        travels = Travel.objects.all()
        return render(request, 'travels/travel_list.html', {'travels':travels})
               

class ApproveTravelAdminView(IsAdmin, View):
    def get(self, request, travel_id):
        travel = get_object_or_404(Travel, id=travel_id)
        travel.approved = True
        travel.save()
        messages.success(request, 'Travel Approved and ticket submitted.', 'success')
        return redirect('travels:travel_detail')
    
                    
class TravelRegisterView(IsAdmin, View):
    travel_form_class = TravelForm
    def get(self, request):
            travel_form = self.travel_form_class
            return render(request, 'travels/travel_admin.html', {'travel_form':travel_form})

    def post(self, request):
        travel_form = self.travel_form_class(request.POST)
        
        if travel_form.is_valid():
            cd = travel_form.cleaned_data
            travel = Travel(driver_car=cd['driver_car'], startcity=cd['startcity'],
                                      destanition=cd['destanition'], date_time=cd['date_time'])
            travel.end_time = travel.get_time
            travel.price = travel.get_cost
            travel.quantity = travel.driver_car.car.capacity
            is_travel_exists = Travel.objects.filter(driver_car=travel.driver_car, 
                                                         date_time__range=[travel.date_time, travel.end_time ]).exists()
            if is_travel_exists:
                messages.error(request, 'driver this time is on travel.', 'danger')
                return render(request, 'travels/raise_error_trip_driver.html', {'travel':travel})
            travel.approved = True
            travel.save()
            messages.success(request, 'New Travel And Ticket Created', 'success')
            return redirect('travels:travel_detail')
        return render(request, 'travels/travel_admin.html', {'travel_form':travel_form})
        
        
class TicketListAdminView(IsAdmin, View):
    def get(self, request, travel_id,*args, **kwargs):
        tickets = Ticket.objects.filter(travel_id=travel_id) # not user & driver!
        return render(request, 'travels/ticket_list.html', {'tickets':tickets})


class TravelListTicketView(IsAdmin, View):
    def get(self, request):
        travels = Travel.objects.all()
        return render(request, 'travels/travel_list_to_ticket.html', {'travels':travels})        
    

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
            return redirect('travels:travel_detail') 
 
 
 
 
