from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse 
from .forms import PostJobForm, QuoteForm, CompleteJobForm, RateJobForm, DisputeForm
from .models import Job, STATUS_CHOICES, FIELD_CHOICES, BiddingOffer, Rating
from accounts.models import User, Message

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
    job = get_object_or_404(Job, pk=job_id)
    if request.user.is_translator and request.user != job.user and job.status == STATUS_CHOICES[0][0]:
        if request.method == 'POST':
            form = QuoteForm(request.POST)
            if form.is_valid():
                existingOffer = BiddingOffer.objects.filter(job = job, translator = request.user).first()
                quote = request.POST["quote"]
                if existingOffer:
                    existingOffer.quote = quote
                    existingOffer.save()   
                else:
                    biddingOffer = BiddingOffer(job=job, translator = request.user, quote = quote)
                    biddingOffer.save()
                message = Message(sender = request.user, receiver = job.user, text = f"{request.user.username} bid {quote} on your job '{job.title}'.")
                message.save()
                return HttpResponseRedirect(reverse('app:job_listing'))        
            else:
                return render(request, 'app/job_bidding.html', {'form': form, 'job': job})
            
        else:
            form = QuoteForm()
            context = {
                'job': job,
                'form': form,
            }
            return render(request, 'app/job_bidding.html', context)
        
    elif request.user.is_authenticated:
        if request.user.is_translator:
            if job.status != STATUS_CHOICES[0][0]:
                error_message = "This job is in progress or finished."
            else:
                error_message = "You cannot bid on your own job."
        else:
            error_message = "You are not a translator."
        jobs = Job.objects.filter(status=STATUS_CHOICES[0][0])
        context = {
            'jobs' : jobs,
            'error_message' : error_message
        }
        return render(request, 'app/job_listing.html', context)
    
    else:
        return HttpResponseRedirect(reverse('accounts:custom_login')) 
    
def job_accept(request, job_id, biddingOffer_id):
    if request.method == "POST":
        job = get_object_or_404(Job, pk = job_id)
        biddingOffer = get_object_or_404(BiddingOffer, pk = biddingOffer_id)
        if (request.user.tokens >= biddingOffer.quote):
            job.translator = biddingOffer.translator
            job.status = STATUS_CHOICES[1][0]

            user = get_object_or_404(User, pk = request.user.id)
            user.tokens -= biddingOffer.quote
            user.save()

            translator = get_object_or_404(User, pk = job.translator.id)
            translator.tokens += biddingOffer.quote  
            translator.save()
            
            job.save()
            message = Message(sender = request.user, receiver = job.translator, text = f"{request.user.username} accepted your bid of {biddingOffer.quote} for job '{job.title}'.")
            message.save()
            BiddingOffer.objects.filter(job=job).exclude(id=biddingOffer_id).delete()
            return HttpResponseRedirect(reverse('accounts:user_dashboard', kwargs={'user_id':request.user.id}))
        else:
            if request.user.is_authenticated:
                jobs = Job.objects.filter(status=STATUS_CHOICES[0][0])
                error_message = "Insufficient tokens."
                context = {
                    'jobs' : jobs,
                    'error_message' : error_message,
                }
                return render(request, 'app/job_listing.html', context)
            else:
                return HttpResponseRedirect(reverse('accounts:custom_login'))

    else:
        return HttpResponseRedirect(reverse('home'))

def complete_job(request, job_id):
    job = get_object_or_404(Job, pk = job_id)
    if request.user == job.translator and job.status == STATUS_CHOICES[1][0]:
        if request.method == "POST":
            form = CompleteJobForm(request.POST)
            if form.is_valid():
                job.translated_text = request.POST['translated_text']
                job.status = STATUS_CHOICES[2][0]
                job.save()
                message = Message(sender = request.user, receiver = job.user, text = f"{request.user.username} completed your job '{job.title}'.")
                message.save()
                return HttpResponseRedirect(reverse('accounts:user_dashboard', kwargs={'user_id':request.user.id}))
            else:
                return render(request, 'app/complete_job.html', {'form':form, 'job':job} )
        else:
            form = CompleteJobForm()
            return render(request, 'app/complete_job.html', {'form':form, 'job':job} )
    else:
        return HttpResponseRedirect(reverse('accounts:custom_login'))
    
def rate_job(request, job_id):
    job = get_object_or_404(Job, pk = job_id)
    if request.user == job.user and job.status == STATUS_CHOICES[2][0]:
        if request.method == "POST":
            form = RateJobForm(request.POST)
            if form.is_valid():
                existingRating = Rating.objects.filter(job = job).first()
                if existingRating:
                    existingRating.rating = request.POST["rating"]
                    existingRating.save()   
                else:
                    rating = Rating(job=job, rating = request.POST["rating"])
                    rating.save()
                return HttpResponseRedirect(reverse('accounts:user_dashboard', kwargs={'user_id':request.user.id}))        
            else:
                return render(request, 'app/rate_job.html', {'form': form, 'job': job})
        else:
            form = RateJobForm()
            return render(request, 'app/rate_job.html', {'form':form, 'job':job})
    else:
        return HttpResponseRedirect(reverse('accounts:custom_login'))
    
def dispute_job(request, job_id):
    job = get_object_or_404(Job, pk = job_id)
    if request.user == job.user and job.status == STATUS_CHOICES[2][0]:
        if request.method == "POST":
            form = DisputeForm(request.POST)
            if form.is_valid():
                dispute = form.save(commit=False)
                dispute.job = job
                dispute.save()
                return HttpResponseRedirect(reverse('accounts:user_profile'))
            else:
                return render(request, 'app/dispute_job.html', {'form':form, 'job': job})
        else:
            form = DisputeForm()
            return render(request, 'app/dispute_job.html', {'form':form, 'job': job})
    else:
        return HttpResponseRedirect(reverse('accounts:custom_login'))
    