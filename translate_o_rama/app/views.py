from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse 
from .forms import PostJobForm, BiddingForm
from .models import Job, STATUS_CHOICES, FIELD_CHOICES, BiddingOffer

# Create your views here.

def home(request):
    context = {}
    return render(request, 'app/home.html', context)

def post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostJobForm(request.POST)
            if form.is_valid():
                job = form.save(commit=False)
                job.user = request.user
                job.save()
                return HttpResponseRedirect(reverse('accounts:custom_login'))
            else:
                return render(request, 'app/post_job.html', {'form': form})
        else:
            form = PostJobForm()
            return render(request, 'app/post_job.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('accounts:custom_login'))  

def job_listing(request):
    if request.user.is_authenticated:
        jobs = Job.objects.filter(status=STATUS_CHOICES[0][0])
        context = {
            'jobs' : jobs,
        }
        return render(request, 'app/job_listing.html', context)
    else:
        return HttpResponseRedirect(reverse('accounts:custom_login'))
    
def job_bidding(request, job_id):
    if request.user.is_translator:
        if request.method == 'POST':
            job = get_object_or_404(Job, pk=job_id)
            form = BiddingForm(request.POST, initial={'job': job, 'translator': request.user}) 
            ## forma nije validna
            
            if form.is_valid():
                existingOffer = BiddingOffer.objects.filter(job = job, translator = request.user).first()
                if existingOffer:
                    existingOffer.quote = request.POST["quote"]
                    existingOffer.save()   
                else:
                    form.save()
                    #biddingOffer = BiddingOffer(job = job, translator = request.user, quote = request.POST["quote"])
                    #biddingOffer.save()
                return HttpResponseRedirect(reverse('accounts:custom_login'))
            else:
                return render(request, 'app/job_bidding.html', {'form': form, 'job': job})
        else:
            job = get_object_or_404(Job, pk=job_id)

            form = BiddingForm()
            context = {
                'job': job,
                'form': form,
            }
            return render(request, 'app/job_bidding.html', context)
    else:
        return HttpResponseRedirect(reverse('accounts:custom_login'))