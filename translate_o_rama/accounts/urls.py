from django.urls import path, include
from . import views

app_name = "accounts"
urlpatterns = [
    path('custom_login/', views.custom_login, name="custom_login"),
]
