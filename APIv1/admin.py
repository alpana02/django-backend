from django.contrib import admin

# Register your models here.

from .models import Website,Sentences
admin.site.register(Website)
admin.site.register(Sentences)