from django.shortcuts import render, redirect
from django.http import HttpResponse
from simplify_main_app.forms import UserForm, CourseForm
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views import View
from simplify_main_app.models import Course, StudentProfile,TutorProfile,User

# Create your views here.
#HomePage
def index(request):
    context_dict ={}
    try:
        course_name = Course.objects.all()
        context_dict['courses']=course_name
    except Course.DoesNotExist:
        context_dict['course']=None
    return render (request, 'simplify_main_app/index.html', context_dict)


#Register Page

def register(request):
    registered=False
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(False)
            user.set_password(user.password)
            user.save()
            registered=True
            if user.role=='STD':
                profile= StudentProfile.objects.update_or_create(user_id=user.id)
            else:
                profile=TutorProfile.objects.update_or_create(user_id=user.id)
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request, 'simplify_main_app/register.html',context={ 'user_form':user_form,
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

@login_required
def student_dashboard(request):
    context_dict ={}
    try:
        course_name = Course.objects.all()
        studentprofile=StudentProfile.objects.all()
        context_dict['courses']=course_name
        context_dict['students']=studentprofile
    except Course.DoesNotExist:
        context_dict['course']=None
        context_dict['students']=None
    return render (request, 'simplify_main_app/dashboard.html', context_dict)

#dashboard view
@login_required
def tutor_dashboard(request):
    context_dict ={}
    try:
        course_name = Course.objects.all()
        tutorprofile= TutorProfile.objects.all()
        context_dict['courses']=course_name
        context_dict['tutors']=tutorprofile
    except Course.DoesNotExist:
        context_dict['course']=None
        context_dict['tutors']=None
    return render (request, 'simplify_main_app/tutor_dashboard.html', context_dict)
    # return render(request, 'simplify_main_app/tutor_dashboard.html')


#logout view
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('simplify_main_app:index'))


class showCourseView(View):
    def get(self,request):
        context_dict ={}
        try:
            course_name = Course.objects.all()
            context_dict['courses']=course_name
        except Course.DoesNotExist:
            context_dict['course']=None

        return render(request,'simplify_main_app/course.html', context_dict)


class addCourseView(View):
    def get(self,request):
        course_form = CourseForm()
        return render(request, 'simplify_main_app/add_course.html', {'form': course_form})
    
    def post(self, request):
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            course_form.save(commit=True)
            return redirect(reverse('simplify_main_app:index'))
        else:
            print(course_form.errors)
            return render(request, 'simplify_main_app/add_course.html', {'form': course_form})
