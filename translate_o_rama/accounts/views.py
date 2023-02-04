from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import SignUpForm, ChangeEmailForm, ChangePasswordForm
from .models import User
from app.models import Job, BiddingOffer, STATUS_CHOICES, Rating


# Create your views here.

def custom_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('login'))
    
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts:custom_login'))
        else:
            return render(request, 'registration/register.html', {'form': form})
    elif not request.user.is_authenticated:
        form = SignUpForm()
        return render(request, 'registration/register.html', {'form': form})
    else:
        return HttpResponseRedirect('/')
    
def user_profile(request):
    if request.user.is_authenticated:
        emailForm = ChangeEmailForm(instance=request.user)
        passwordForm = ChangePasswordForm(request.user)
        return render(request, 'registration/user_profile.html', {'emailForm': emailForm, 'passwordForm': passwordForm})
    else:
        return HttpResponseRedirect(reverse('accounts:custom_login'))

def change_email(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ChangeEmailForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('accounts:user_profile'))
            else:
                passwordForm = ChangePasswordForm(request.user)
                return render(request, 'registration/user_profile.html', {'emailForm': form, 'passwordForm': passwordForm})
        else:
            return HttpResponseRedirect(reverse('accounts:user_profile'))
    else:
        return HttpResponseRedirect(reverse('accounts:custom_login'))

def change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ChangePasswordForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('accounts:user_profile'))
            else:
                emailForm = ChangeEmailForm(instance=request.user)
                return render(request, 'registration/user_profile.html', {'emailForm': emailForm, 'passwordForm': form})
        else:
            return HttpResponseRedirect(reverse('accounts:user_profile'))
    else:
        return HttpResponseRedirect(reverse('accounts:custom_login'))
    
def user_dashboard(request, user_id):
    if request.user.is_authenticated:
        target_user = get_object_or_404(User, pk = user_id)
        postedJobs = Job.objects.filter(user = target_user).filter(status= STATUS_CHOICES[0][0])
        assignedJobsUser = Job.objects.filter(user = target_user).filter(status = STATUS_CHOICES[1][0])
        assignedJobsTranslator = Job.objects.filter(translator = target_user).filter(status = STATUS_CHOICES[1][0])
        completedJobsUser = Job.objects.filter(user = target_user).filter(status = STATUS_CHOICES[2][0])
        completedJobsTranslator = Job.objects.filter(translator = target_user).filter(status = STATUS_CHOICES[2][0])
        biddingOffers = BiddingOffer.objects.all()
        
        sum = 0
        counter = 0
        for completedJob in completedJobsTranslator:
            if (completedJob.rating_set.first()):
                sum += completedJob.rating_set.first().rating
                counter += 1   

        if counter != 0:
            rating = sum/counter
        else:
            rating = None

        context = {
            'target_user' : target_user,
            'postedJobs' : postedJobs,
            'assignedJobsUser': assignedJobsUser,
            'assignedJobsTranslator': assignedJobsTranslator,
            'completedJobsUser': completedJobsUser,
            'completedJobsTranslator' : completedJobsTranslator,
            'biddingOffers' : biddingOffers,
            'rating' : rating,
        }
        return render(request, 'registration/user_dashboard.html', context)
    else:
        return HttpResponseRedirect(reverse('accounts:custom_login'))
