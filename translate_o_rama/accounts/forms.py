from django import forms
from accounts.models import User, Message
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, UserChangeForm
from django.forms import ModelForm, ValidationError
from django.contrib.auth.password_validation import validate_password




class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    is_translator = forms.BooleanField(label = 'Translator', required=False)
    username = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ( 'email', 'username', 'is_translator', 'password1', 'password2' )

    


class ChangeEmailForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(ChangeEmailForm, self).__init__(*args, **kwargs)
        del self.fields['password']

class ChangePasswordForm(SetPasswordForm):

    class Meta:
        model = User
        fields = ('new_password1', 'new_password2')

class SendMessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ('text',)


    
    
        