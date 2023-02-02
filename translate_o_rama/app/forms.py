from .models import Job
from django.forms import ModelForm



class PostJobForm(ModelForm):
    class Meta:
        model = Job
        exclude = ('user', 'translator', 'translated_text', 'status')
    