from django.contrib import admin
from .models import User, Message

class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'password', 'is_translator', 'tokens')
    list_display = ('email', 'username', 'is_translator', 'tokens')

class MessageAdmin(admin.ModelAdmin):
    fields = ('sender', 'receiver', 'text')
    list_display = ('sender', 'receiver', 'text', 'time')

admin.site.register(User,UserAdmin)
admin.site.register(Message,MessageAdmin)

