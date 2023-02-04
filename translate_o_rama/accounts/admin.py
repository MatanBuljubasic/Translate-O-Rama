from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'password', 'is_translator', 'tokens')
    list_display = ('email', 'username', 'is_translator', 'tokens')

admin.site.register(User,UserAdmin)

