from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import SignUpForm

# Create your views here.

def custom_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/admin')
    else:
        return HttpResponseRedirect(reverse('login'))
    
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = SignUpForm()


    return render(request, 'registration/signup.html', {'form': form})
    