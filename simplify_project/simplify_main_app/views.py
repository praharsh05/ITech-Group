from django.shortcuts import render, redirect
from django.http import HttpResponse
from simplify_main_app.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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

#Login view
def user_login(request):
    if request.method =='POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            #is the account active? it could have been disabled
            if user.is_active:
                #if the account is valid and active we can log the user in
                #we will send the user back to homepage
                login(request,user)
                return redirect(reverse('simplify_main_app:index'))
            else:
                #an inactive account was used - no longer loging in
                return HttpResponse("Your Simplify account is disabled.")
        else:
            #bad login details were provided, so we can't log user in
            print(f"Invalid user details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    #the request is not an HTTP POST so return a login form
    #this is most likly HTTP GET
    else:
        #no context variable to pass to the template system hence blank dict
        return render(request, 'simplify_main_app/login.html')

# Profile page
def forum(request):
    context = {}
    return render(request, 'simplify_main_app/forum.html', context)

#dashboard view
# @login_required
def dashboard(request):
    context = {}
    return render(request, 'simplify_main_app/dashboard.html', context)


#logout view
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('simplify_main_app:index'))

