from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_translator = models.BooleanField('Translator', default=False)
    email = models.EmailField('Email', unique=True)
    username = models.CharField('Username', unique=False, max_length=30)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'is_translator']

