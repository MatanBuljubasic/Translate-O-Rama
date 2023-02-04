from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import SignUpForm, ChangeEmailForm, ChangePasswordForm, SendMessageForm
from .models import User, Message
from app.models import Job, BiddingOffer, STATUS_CHOICES


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
        assignedJobsUser = Job.objects.filter(user = request.user).filter(status = STATUS_CHOICES[1][0])
        assignedJobsTranslator = Job.objects.filter(translator = request.user).filter(status = STATUS_CHOICES[1][0])
        completedJobsUser = Job.objects.filter(user = request.user).filter(status = STATUS_CHOICES[2][0])
        completedJobsTranslator = Job.objects.filter(translator = request.user).filter(status = STATUS_CHOICES[2][0])

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
            'emailForm': emailForm,
            'passwordForm': passwordForm,
            'assignedJobsUser': assignedJobsUser,
            'assignedJobsTranslator': assignedJobsTranslator,
            'completedJobsUser': completedJobsUser,
            'completedJobsTranslator' : completedJobsTranslator,
            'rating' : rating,
            }
        return render(request, 'registration/user_profile.html', context)
    else:
        return HttpResponseRedirect(reverse('accounts:custom_login'))

def change_email(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            currentEmail = request.user.email
            form = ChangeEmailForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('accounts:user_profile'))
            else:
                request.user.email = currentEmail
                passwordForm = ChangePasswordForm(request.user)
                assignedJobsUser = Job.objects.filter(user = request.user).filter(status = STATUS_CHOICES[1][0])
                assignedJobsTranslator = Job.objects.filter(translator = request.user).filter(status = STATUS_CHOICES[1][0])
                completedJobsUser = Job.objects.filter(user = request.user).filter(status = STATUS_CHOICES[2][0])
                completedJobsTranslator = Job.objects.filter(translator = request.user).filter(status = STATUS_CHOICES[2][0])

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
                    'emailForm': form,
                    'passwordForm': passwordForm,
                    'assignedJobsUser': assignedJobsUser,
                    'assignedJobsTranslator': assignedJobsTranslator,
                    'completedJobsUser': completedJobsUser,
                    'completedJobsTranslator' : completedJobsTranslator,
                    'rating' : rating,
                    }
                return render(request, 'registration/user_profile.html', context)
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
                assignedJobsUser = Job.objects.filter(user = request.user).filter(status = STATUS_CHOICES[1][0])
                assignedJobsTranslator = Job.objects.filter(translator = request.user).filter(status = STATUS_CHOICES[1][0])
                completedJobsUser = Job.objects.filter(user = request.user).filter(status = STATUS_CHOICES[2][0])
                completedJobsTranslator = Job.objects.filter(translator = request.user).filter(status = STATUS_CHOICES[2][0])

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
                    'emailForm': emailForm,
                    'passwordForm': form,
                    'assignedJobsUser': assignedJobsUser,
                    'assignedJobsTranslator': assignedJobsTranslator,
                    'completedJobsUser': completedJobsUser,
                    'completedJobsTranslator' : completedJobsTranslator,
                    'rating' : rating,
                    }
                return render(request, 'registration/user_profile.html', context)
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
        messages = Message.objects.filter(receiver = target_user).order_by('-time')
        submittedBids = biddingOffers.filter(translator = target_user).filter(job__status = STATUS_CHOICES[0][0])
        
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
            'messages' : messages,
            'submittedBids' : submittedBids
        }
        return render(request, 'registration/user_dashboard.html', context)
    else:
        return HttpResponseRedirect(reverse('accounts:custom_login'))
    
def send_message(request, user_id, target_user_id):
    messageSender = get_object_or_404(User, pk = user_id)
    messageReceiver = get_object_or_404(User, pk = target_user_id)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = SendMessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.sender = messageSender
                message.receiver = messageReceiver
                message.save()
                return HttpResponseRedirect(reverse('accounts:user_dashboard', kwargs={'user_id':target_user_id}))
            else:
                context = {
                    'form' : form,
                    'messageReceiver' : messageReceiver
                }
                return render(request, 'registration/send_message.html', context)
        else:
            if messageReceiver != messageSender:
                form = SendMessageForm()
                context = {
                    'form' : form,
                    'messageReceiver' : messageReceiver
                }
                return render(request, 'registration/send_message.html', context)
            else:
                return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('accounts:custom_login'))
