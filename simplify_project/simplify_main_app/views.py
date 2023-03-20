from django.shortcuts import render, redirect
from django.http import HttpResponse
from simplify_main_app.forms import UserForm, CourseForm, ProfileForm
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views import View
from simplify_main_app.models import Course, StudentProfile,TutorProfile,User,Profile
from django.db.models import Q
import populate_courses
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
                if user.role=='TUT':
                    return redirect(reverse('simplify_main_app:tutor-dashboard'))
                else:
                    return redirect('simplify_main_app:student-dashboard')
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
    # if request.method =='POST':
    #     username= request.POST.get('username')
    #     id = request.POST.get('course_id')
    #     for u in User.objects.all():
    #         if (u.username == username):
    #             t=StudentProfile.objects.get_or_create(course_id=id,user=u)
    try:
        id=request.user.id
        course_name = Course.objects.all()
        #studentprofile=StudentProfile.objects.get(user_id=id)
        context_dict['courses']=course_name
        #context_dict['students']=studentprofile
        context_dict['courseid']=StudentProfile.objects.filter(Q(user_id=id))
    except Course.DoesNotExist:
        context_dict['course']=None
        #context_dict['students']=None
        context_dict['courseid']=None
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
    def get(self,request,course_name_slug):
        context_dict =self.helper(course_name_slug)
        return render(request,'simplify_main_app/course.html', context_dict)
    
    def helper(self,course_name_slug):
        context_dict = {}
        try:
            course = Course.objects.get(slug=course_name_slug)
            materials = Material.objects.filter(material=course)
            context_dict['materials']=materials
            context_dict['course']=course
        except Course.DoesNotExist:
            context_dict['materials']=None
            context_dict['course']=None
        return context_dict


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
class ProfileView(View):
    
    def get(self,request):
        profileform = ProfileForm()
        return render(request, 'simplify_main_app/profile.html', {'form': profileform})
        
    def post(self, request):
        profileform = ProfileForm(request.POST)

        if profileform.is_valid():
            profileform.save(commit=True)
            i=request.user.id
            t=request.profileform.id
            #populate_courses.updateProfile(i)
            u=User.objects.update_or_create(id=i,first_name=request.POST.get('firstname'),last_name=request.POST.get('lastname'))
            # u.first_name=p.firstname
            # u.last_name=p.lastname
            # print(u.first_name)
            # u.save()
            
            if User.role=='STD':
                
                return redirect(reverse('simplify_main_app:student-dashboard'))
            else:
                return redirect(reverse('simplify_main_app:tutor-dashboard'))
        else:
            print(ProfileForm.errors)
            return render(request, 'simplify_main_app/profile.html', {'form': profileform})
# def ProfileView(request):
#     profileform = ProfileForm()
#     if request.method == 'POST':
#         profileform = ProfileForm(request.POST)
#         if profileform.is_valid():
#             profileform.save(False)
#             i=request.user.id
#             u=User.objects.get(id=i)
#             u.first_name=request.POST.get('firstname')
#             u.last_name=request.POST.get('lastname')
#             print(u.first_name)
#             u.save()
#             print(u.first_name)
#             if User.role=='STD':
                
#                 return redirect(reverse('simplify_main_app:student-dashboard'))
#             else:
#                 return redirect(reverse('simplify_main_app:tutor-dashboard'))
#     else:
#         print(ProfileForm.errors)
#         return render(request, 'simplify_main_app/profile.html', {'form': profileform})

    