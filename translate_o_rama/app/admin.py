from django.contrib import admin
from .models import Job

# Register your models here.

class JobAdmin(admin.ModelAdmin):
    list_display = ('user','translator', 'title', 'budget', 'status')
    exclude = ('translated_text', )

admin.site.register(Job, JobAdmin)
