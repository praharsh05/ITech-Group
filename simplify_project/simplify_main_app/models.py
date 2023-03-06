from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#creating a databse for users
class UserProfile(models.Model):
    
    std = 'STD'
    tut = 'TUT'
    typeChoice = [(std, 'Student'),
                  (tut, 'Tutor')]
    user = models.OneToOneField(User ,related_name='user_profile', on_delete=models.CASCADE)
    type = models.CharField(max_length=3, choices=typeChoice, default=std, blank=False)

    def __str__(self):
        return self.user.username

