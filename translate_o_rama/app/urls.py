from django.urls import path, include
from . import views

app_name = "app"
urlpatterns = [
    path('post/',  views.post,  name="post"),
    path('job_listing/', views.job_listing, name="job_listing"),
]
