from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse 
from .forms import PostJobForm
from .models import Job, STATUS_CHOICES, FIELD_CHOICES

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