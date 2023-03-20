from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

# Create your models here.

#creating a databse for users

class User(AbstractUser):
    class Role(models.TextField):
        STUDENT = 'STD'
        TUTOR = 'TUT'
        typeChoice = [(STUDENT, 'Student'),
                    (TUTOR, 'Tutor')]

    role = models.CharField(max_length=3, choices=Role.typeChoice,blank=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            return super().save(*args, **kwargs)

#to query student
class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STUDENT)

#proxy table for student
class Student(User):
    base_role = User.Role.STUDENT
    student = StudentManager()
    class Meta:
        proxy = True

#on creation of the a student instance in user table create an entry in student profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    print('inside create user profile for student')
    if created and instance.role == 'STD':
        StudentProfile.objects.create(user=instance)
        instance.save()

#to query tutor table
class TutorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.TUTOR)


class Tutor(User):
    base_role = User.Role.TUTOR
    tutor = TutorManager()
    class Meta:
        proxy = True

#tutor profile
# class TutorProfile(models.Model):
#     course_id = models.IntegerField(null=True, blank=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     # tutor_id = models.IntegerField(null=True, blank=True)
    

#on creation of tutor user do this
@receiver(post_save, sender=Tutor)
def create_user_profile(sender, instance, created, **kwargs):
    print('inside create user profile for tutor')
    if created and instance.role == 'TUT':
        TutorProfile.objects.create(user=instance)
        instance.save()



class Course(models.Model):
    tutor = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=128)
    introduction = models.CharField(max_length=1024)
    slug= models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug= slugify(self.course_name)
        super(Course, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Courses'
    
    def __str__(self):
        return self.course_name
    
class Material(models.Model):
    material = models.ForeignKey(Course, on_delete=models.CASCADE)
    url = models.URLField()
class Profile(models.Model):
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    def save(self, *args, **kwargs):
        super(Profile,self).save(*args,**kwargs)

    class Meta:
        verbose_name_plural = 'Profiles'
    
    def __str__(self):
        return self.url
    def __str__(self):
        return self.firstname 


#tutor profile
class TutorProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course= models.OneToOneField(Course,null=True, blank=True,default=None, on_delete=models.CASCADE)


#student profile
class StudentProfile(models.Model):
    course= models.ManyToManyField(Course, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # student_id = models.IntegerField(null=True, blank=True)

