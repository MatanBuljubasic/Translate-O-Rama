from django.urls import path, include
from . import views

app_name = "app"
urlpatterns = [
    path('post/',  views.post,  name="post"),
]
