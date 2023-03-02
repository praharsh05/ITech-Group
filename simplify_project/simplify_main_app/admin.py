from django.contrib import admin
from simplify_main_app.models import UserProfile

# Register your models here.

#registering the view in the admin for user profiles
admin.site.register(UserProfile)
