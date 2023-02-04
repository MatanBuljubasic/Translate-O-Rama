from decimal import Decimal
from .models import Job, BiddingOffer, Dispute
from django.forms import ModelForm, ValidationError
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class PostJobForm(ModelForm):
    class Meta:
        model = Job
        exclude = ('user', 'translator', 'translated_text', 'status')

    def clean(self):
        super(PostJobForm, self).clean()   
        source_language = self.cleaned_data['source_language']
        target_language = self.cleaned_data['target_language']
        if source_language == target_language:
            self.add_error("source_language", "Source and target language can't be the same.")
        return self.cleaned_data
    

class QuoteForm(forms.Form):   
    quote = forms.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0.01'))])

class CompleteJobForm(forms.Form):
    translated_text = forms.CharField(widget=forms.Textarea(),required=True)

class RateJobForm(forms.Form):
    rating = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
class DisputeForm(ModelForm):
    class Meta:
        model = Dispute
        fields = ('reason',)



        
