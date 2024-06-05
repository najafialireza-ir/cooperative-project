from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from orders.models import Ticket


class HomeView(View):
    def get(self, request):
        ticket = Ticket.objects.all()
        return render(request, 'homep/home.html', {'tickets':ticket})
        