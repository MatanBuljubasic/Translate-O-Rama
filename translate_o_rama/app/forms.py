from decimal import Decimal
from .models import Job, BiddingOffer
from django.forms import ModelForm, ValidationError
from django import forms
from django.core.validators import MinValueValidator

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
    

class QuoteForm(forms.Form):   
    quote = forms.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0.01'))])


        
