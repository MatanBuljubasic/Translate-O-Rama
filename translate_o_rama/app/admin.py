from django.contrib import admin
from .models import Job, BiddingOffer

# Register your models here.

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'translator', 'budget', 'status')
    exclude = ('translated_text', )

class BiddingOfferAdmin(admin.ModelAdmin):
    list_display = ('job', 'translator', 'quote')
    exclude = ()

admin.site.register(Job, JobAdmin)
admin.site.register(BiddingOffer, BiddingOfferAdmin)

