from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

# Create your models here.

#creating a databse for users

# model to have user details, it extends the AbstractUser class
class User(AbstractUser):

    #defining a child class/ subclass role in order to have 2 different roles for the users
    class Role(models.TextField):
        STUDENT = 'STD'
        TUTOR = 'TUT'
        typeChoice = [(STUDENT, 'Student'),
                    (TUTOR, 'Tutor')]

    #role field making use of the choices from the upper child class/subclass
    role = models.CharField(max_length=3, choices=Role.typeChoice,blank=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            return super().save(*args, **kwargs)


#table for course created by a tutor
class Course(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
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


#table for the matrials in a course
class Material(models.Model):
    material = models.ForeignKey(Course, on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return self.url
    

class Profile(models.Model):
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)


    def save(self, *args, **kwargs):
        super(Profile,self).save(*args,**kwargs)

    class Meta:
        verbose_name_plural = 'Profiles'
    
    def __str__(self):
        return self.firstname 


#tutor profile
class TutorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course= models.ManyToManyField(Course, blank=True,default=None)


#student profile
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course= models.ManyToManyField(Course, blank=True, default=None)
    

