from django.shortcuts import render
from django.http import HttpResponse
from simplify_main_app.forms import UserForm, UserProfileForm

# Create your views here.
#HomePage
def index(request):
    context_dict = {}
    response = render(request, 'simplify_main_app/index.html', context=context_dict)
    return response


#Register Page

def register(request):
    registered=False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered=True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'simplify_main_app/register.html',context={ 'user_form':user_form,
                                                                      'profile_form':profile_form,
                                                                      'registered':registered})
