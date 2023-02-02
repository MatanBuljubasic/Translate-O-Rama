from .models import Job
from django.forms import ModelForm, ValidationError



class PostJobForm(ModelForm):
    class Meta:
        model = Job
        exclude = ('user', 'translator', 'translated_text', 'status')

    def clean(self):
        source_language = self.cleaned_data['source_language']
        target_language = self.cleaned_data['target_language']
        if source_language == target_language:
            self.add_error("source_language", "Traženi jezik i zadani jezik su jednaki.")
        return self.cleaned_data
    