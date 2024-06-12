from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    #Zeige die info beim anklicken an
    fields = ('text','create_at', 'author', 'receiver')
    #Zeige die Info als Tabelle beim laden an 
    list_display = ('text','create_at', 'author', 'receiver')
    #CustomFilter
    search_fields = ('text',)

# Register your models here.
admin.site.register(Message, MessageAdmin)