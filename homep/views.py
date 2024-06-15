from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from travels.models import Travel


class HomeView(View):
    def get(self, request):
        travels = Travel.objects.all()
        try:
            param = request.GET.get('filter_by')
            if param == 'bus':
                travels = travels.filter(driver_car__car__name='bus').order_by('-date_time')
                return render(request, 'homep/home.html', {'travels':travels})
            elif param == 'van':
                travels = travels.filter(driver_car__car__name='van').order_by('-date_time')
                return render(request, 'homep/home.html', {'travels':travels})
        except:
            pass
        return render(request, 'homep/home.html', {'travels':travels})
        