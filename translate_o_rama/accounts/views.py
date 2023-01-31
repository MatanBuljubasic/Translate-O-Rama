from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def custom_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/admin')
    else:
        return HttpResponseRedirect(reverse('login'))