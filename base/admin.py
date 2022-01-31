from django.contrib import admin

# Register your models here.

from .models import Note, Topic, Message

admin.site.register(Note) 
admin.site.register(Topic)
admin.site.register(Message)