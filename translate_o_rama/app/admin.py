from django.contrib import admin
from .models import Job

# Register your models here.

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'translator', 'budget', 'status')
    exclude = ('translated_text', )

admin.site.register(Job, JobAdmin)
