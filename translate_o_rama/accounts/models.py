from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_translator = models.BooleanField('Translator', default=False)
    email = models.EmailField('Email', unique=True)
    username = models.CharField('Username', unique=False, max_length=30)
    tokens = models.DecimalField('Token balance', decimal_places=2, max_digits=10, default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'is_translator']

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.sender} to {self.receiver}"

