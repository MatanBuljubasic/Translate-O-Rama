from django import forms
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    is_translator = forms.BooleanField(label = 'Translator')

    class Meta:
        model = User
        fields = ( 'email', 'username', 'is_translator', 'password1' ,'password2' )

    
    
        