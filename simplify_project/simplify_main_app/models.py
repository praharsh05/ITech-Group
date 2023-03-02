from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#creating a databse for users
class UserProfile(models.Model):
    
    std = 'STD'
    tut = 'TUT'
    typeChoice = [(std, 'Student'),
                  (tut, 'Tutor')]
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    firstName = models.CharField(max_length=128, blank=False)
    lastName = models.CharField(max_length=128, blank= False)
    type = models.CharField(max_length=3, choices=typeChoice, default=std, blank=False)

    def __str__(self):
        return self.user.username

