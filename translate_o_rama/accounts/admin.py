from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'password', 'is_translator')
    list_display = ('email', 'username', 'is_translator')

admin.site.register(User,UserAdmin)

