from django import forms

from django.forms import ModelForm, TextInput, EmailInput, Select

# from django.contrib.auth.models import User
from simplify_main_app.models import User, Course, Material, StudentProfile, Profile



#creating a user form to get details
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','style': 'max-width: 300px;'}))#using the widget to hide password on input


    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control','style': 'max-width: 300px;'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control','style': 'max-width: 300px;'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password','first_name', 'last_name', )
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

             'role': Select(attrs={
                'class': "form-select",
                'style': 'max-width: 120px;'
            })
        }
    
class ProfileForm(forms.ModelForm):
    firstname = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control','style': 'max-width: 300px;'}),
                                help_text="Enter First Name")
    lastname = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control','style': 'max-width: 300px;'}),
                               help_text="Enter Last Name")

    class Meta:
        model = Profile
        fields ={'firstname', 'lastname'}

class CourseForm(forms.ModelForm):
    course_name = forms.CharField(max_length=128, help_text="Please enter course name")
    introduction = forms.CharField(max_length=1024,help_text="Please enter course introduction")

    class Meta:
        model = Course
        fields ={'course_name','introduction'}


#form for adding a URL in the material field
class MaterialForm(forms.ModelForm):
    url = forms.URLField(help_text="Please enter the URL of the material")

    class Meta:
        model=Material
        exclude = ('material',)

    def clean(self):#taken from tango with django book
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        # if url is not empty and does not start with 'http://',
        #then prepend 'http://'
        if url and not (url.startswith('http://') or url.startswith('https://')):
            url = f'http://{url}'
            cleaned_data['url'] = url

        return cleaned_data

