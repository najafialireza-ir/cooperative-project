from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from travels.models import Travel


class HomeView(View):
    def get(self, request):
        travels = Travel.objects.all()
        return render(request, 'homep/home.html', {'travels':travels})
        