from django.contrib import admin
from home.models import Meet, Messages

admin.site.register((Meet, Messages))