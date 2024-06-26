from django.contrib import admin
from .models import Recipe,Feedback,Notification
# Register your models here.
admin.site.register(Recipe)
admin.site.register(Feedback)
admin.site.register(Notification)