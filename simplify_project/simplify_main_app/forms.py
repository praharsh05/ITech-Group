from django import forms
from simplify_main_app.models import User


#creating a user form to get details
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)#using the widget to hide password on input

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ('username', 'password','first_name', 'last_name','role')
