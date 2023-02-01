from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import SignUpForm, ChangeEmailForm, ChangePasswordForm


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
    elif not request.user.is_authenticated:
        form = SignUpForm()
        return render(request, 'registration/register.html', {'form': form})
    else:
        return HttpResponseRedirect('/')
    
def user_profile(request, error_message=0):
    if request.user.is_authenticated:
        emailForm = ChangeEmailForm(instance=request.user)
        passwordForm = ChangePasswordForm(request.user)
        return render(request, 'registration/user_profile.html', {'emailForm': emailForm, 'passwordForm': passwordForm, 'error_message':error_message})
    else:
        return HttpResponseRedirect(reverse('accounts:custom_login'))

def change_email(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ChangeEmailForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('accounts:user_profile', args=[0]))
        else:
            return HttpResponseRedirect(reverse('accounts:user_profile', args=[0]))
    else:
        return HttpResponseRedirect(reverse('accounts:custom_login'))

def change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ChangePasswordForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('accounts:user_profile', args=[0]))
            else:
                return HttpResponseRedirect(reverse('accounts:user_profile', args=[1]))
        else:
            return HttpResponseRedirect(reverse('accounts:user_profile', args=[0]))
    else:
        return HttpResponseRedirect(reverse('accounts:custom_login'))
