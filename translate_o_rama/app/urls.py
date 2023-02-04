from django.urls import path, include
from . import views

app_name = "app"
urlpatterns = [
    path('post/', views.post,  name="post"),
    path('job_listing/', views.job_listing, name="job_listing"),
    path('job_listing/<int:job_id>', views.job_bidding, name="job_bidding"),
    path('job_accept/<int:job_id>/<int:biddingOffer_id>', views.job_accept, name="job_accept"),
    path('complete_job/<int:job_id>', views.complete_job, name="complete_job"),
    path('rate_job/<int:job_id>', views.rate_job, name="rate_job"),
    path('dispute_job/<int:job_id>', views.dispute_job, name="dispute_job"),
]
