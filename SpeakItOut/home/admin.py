from django.contrib import admin
from home.models import Meet, Message

admin.site.register((Meet, Message))