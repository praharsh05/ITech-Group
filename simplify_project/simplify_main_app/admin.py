from django.contrib import admin
from simplify_main_app.models import User, Course,Material

# Register your models here.

#registering the model in the admin for user
admin.site.register(User)


# for course admin
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('course_name',)}

#for materials in a course
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('material', 'url')


# registering the model
admin.site.register(Course,CourseAdmin)
admin.site.register(Material,MaterialAdmin)
