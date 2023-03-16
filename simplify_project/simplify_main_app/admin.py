from django.contrib import admin
from simplify_main_app.models import User

# Register your models here.

#registering the view in the admin for user
admin.site.register(User)
