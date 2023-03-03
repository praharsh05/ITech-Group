from django import forms
from django.contrib.auth.models import User
from simplify_main_app.models import UserProfile


#creating a user form to get details
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)#using the widget to hide password on input

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password','first_name', 'last_name', )

#creating another form to get the type
class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('type',)