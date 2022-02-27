from django.contrib import admin

# Register your models here.

from tasks.models import Task, UserProfile

admin.sites.site.register(UserProfile)
admin.sites.site.register(Task)
