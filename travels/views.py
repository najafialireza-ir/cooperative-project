from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from management.models import DriverCar
from travels.models import Travel, Ticket
from django.contrib import messages
from utils import IsAdmin
from .forms import TravelForm, TravelRegisterDriverForm
import datetime

class TravelDetailUserView(View):
    """ ticket detail show for normal user"""   
    def get(self, request, *args, **kwargs):
        tickets = Ticket.objects.filter(travel_id=kwargs['travel_id'])
        return render(request, 'travels/ticket_list_user.html', {'tickets':tickets})
    
 
class DriverRegisterTravel(LoginRequiredMixin, View):
    travel_form = TravelRegisterDriverForm
    def get(self, request, *args, **kwargs):
        if request.user.user_type == '2':
            travel_form = self.travel_form
            return render(request, 'travels/driver_register_travel.html', {'travel_form':travel_form})
                 
    def post(self, request, *args, **kwargs):
        if request.user.user_type == '2':
            travel_form = self.travel_form(request.POST)
            if travel_form.is_valid():
                cd = travel_form.cleaned_data         
                time = cd['time']
                date = cd ['date']
                date_time = datetime.datetime.combine(date, time)   
                driver = DriverCar.objects.get(driver__user_id=request.user.id)
                travel = Travel(driver_car=driver, startcity=cd['startcity'],
                                      destanition=cd['destanition'], date_time=date_time)
                if travel.get_distance != 0:
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
                    return redirect('accounts:driver_travel', driver.id)
                
                messages.error(request, 'startcity and destination can`t the same!', 'danger')
                return render(request, 'travels/driver_register_travel.html', {'travel_form':travel_form})
                
            messages.error(request, 'you must complete this form!', 'danger')
            return render(request, 'travels/driver_register_travel.html', {'travel_form':travel_form})
        messages.error(request, 'You don`t access this page.', 'danger')
        return redirect('home:home')


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
            return render(request, 'travels/travel_admin_register.html', {'travel_form':travel_form})

    def post(self, request):
        travel_form = self.travel_form_class(request.POST)
        
        if travel_form.is_valid():
            cd = travel_form.cleaned_data
            time = cd['time']
            date = cd ['date']
            date_time = datetime.datetime.combine(date, time)
            travel = Travel(driver_car=cd['driver_car'], startcity=cd['startcity'],
                                      destanition=cd['destanition'], date_time=date_time)
            if travel.get_distance != 0:
                travel.end_time = travel.get_time
                travel.price = travel.get_cost
                travel.quantity = travel.driver_car.car.capacity
                is_travel_exists = Travel.objects.filter(driver_car=travel.driver_car, 
                                                            date_time__range=[travel.date_time, travel.end_time ]).exists()
                print(Travel.objects.filter(driver_car=travel.driver_car, 
                                                            date_time__range=[travel.date_time, travel.end_time ]))
                if is_travel_exists:
                    messages.error(request, 'driver this time is on travel.', 'danger')
                    return render(request, 'travels/raise_error_trip_driver.html', {'travel':travel})
                travel.approved = True
                travel.save()
                messages.success(request, 'New Travel And Ticket Created', 'success')
                return redirect('travels:travel_detail')
            messages.error(request, 'startcity and destination can`t the same!!', 'danger')
            return render(request, 'travels/travel_admin_register.html', {'travel_form':travel_form})
        
        messages.error(request, 'you must complete this form!', 'danger')
        return render(request, 'travels/travel_admin_register.html', {'travel_form':travel_form})
        
        
class TicketListAdminView(IsAdmin, View):
    def get(self, request, travel_id,*args, **kwargs):
        tickets = Ticket.objects.filter(travel_id=travel_id) 
        return render(request, 'travels/ticket_list_admin_panel.html', {'tickets':tickets})


class TravelListTicketView(IsAdmin, View):
    def get(self, request):
        travels = Travel.objects.all().reverse()
        return render(request, 'travels/travel_list_to_ticket.html', {'travels':travels})        
    
class TravelListView(IsAdmin, View):
    def get(self, request):
        travels = Travel.objects.all().reverse()
        return render(request, 'travels/travel_list_admin.html', {'travels':travels})
               

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
 
 
 
 
