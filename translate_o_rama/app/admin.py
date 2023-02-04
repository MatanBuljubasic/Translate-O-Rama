from django.contrib import admin
from .models import Job, BiddingOffer, Rating, Dispute

# Register your models here.

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'translator', 'budget', 'status')
    exclude = ('translated_text', )

class BiddingOfferAdmin(admin.ModelAdmin):
    list_display = ('job', 'translator', 'quote')
    exclude = ()

class RatingAdmin(admin.ModelAdmin):
    list_display = ('job', 'rating')
    exclude = ()

class DisputeAdmin(admin.ModelAdmin):
    list_display = ('job', 'status')
    exclude = ()

admin.site.register(Job, JobAdmin)
admin.site.register(BiddingOffer, BiddingOfferAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Dispute, DisputeAdmin)

