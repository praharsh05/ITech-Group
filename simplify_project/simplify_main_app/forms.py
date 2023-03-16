from django import forms

from django.forms import ModelForm, TextInput, EmailInput, Select
from django.contrib.auth.models import User
from simplify_main_app.models import UserProfile



#creating a user form to get details
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','style': 'max-width: 300px;'}))#using the widget to hide password on input


    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control','style': 'max-width: 300px;'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control','style': 'max-width: 300px;'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password','first_name', 'last_name','role', )
        # style of the form
        widgets = {
            'username': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;'
                }),
            'email': EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;'
                }),
             'type': Select(attrs={
                'class': "form-select",
                'style': 'max-width: 120px;'
            })
        }
    

