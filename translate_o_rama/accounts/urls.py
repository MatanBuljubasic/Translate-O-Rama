from django.urls import path, include
from . import views

app_name = "accounts"
urlpatterns = [
    path('custom_login/', views.custom_login, name="custom_login"),
    path('register/', views.register, name="register"),
    path('user_profile/<int:error_message>/', views.user_profile, name="user_profile"),
    path('change_email/', views.change_email, name="change_email"),
    path('change_password/', views.change_password, name="change_password"),
]
