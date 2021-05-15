from django.contrib import admin
from home.models import Meet, Message, Buffer

admin.site.register((Meet, Message, Buffer))