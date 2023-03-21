from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from simplify_main_app.forms import UserForm, CourseForm,MaterialForm, ProfileForm
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from simplify_main_app.models import Course, StudentProfile,TutorProfile,User,Profile, Material
from django.db.models import Q

# Create your views here.

#HomePage view
class IndexView(View):
    #get request for index page
    def get(self, request):
        context_dict ={}
        try:
            course_name = Course.objects.all()
            context_dict['courses']=course_name
        except Course.DoesNotExist:
            context_dict['course']=None
        return render (request, 'simplify_main_app/index.html', context_dict)


#Register Page view
class RegisterView(View):
    #get the register form
    def get(self,request):
        registered=False
        user_form = UserForm()
        return render(request, 'simplify_main_app/register.html',context={ 'user_form':user_form,
                                                                      'registered':registered})

    #post the register form
    def post(self,request):
        registered=False
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            
            if user.role=='STD':
                profile= StudentProfile.objects.update_or_create(user_id=user.id)
            else:
                profile=TutorProfile.objects.update_or_create(user_id=user.id)
            registered=True
            return render(request, 'simplify_main_app/login.html')
        else:
            print(user_form.errors)
        return render(request, 'simplify_main_app/register.html',context={ 'user_form':user_form,
                                                                      'registered':registered})

#Login view
class LoginView(View):
    #if request is get send the log in form
    def get(self,request):
        return render(request, 'simplify_main_app/login.html')
    
    #if request is post then check and log user in
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        #authenticate teh username and password recieved
        user = authenticate(username = username, password = password)
        if user:
            #is the account active? it could have been disabled
            if user.is_active:
                #if the account is valid and active we can log the user in
                #we will send the user to the respective dashboard
                login(request,user)
                #if user is a tutor
                if user.role=='TUT':
                    return redirect(reverse('simplify_main_app:tutor-dashboard'))
                else:#else if the user is student
                    return redirect('simplify_main_app:student-dashboard')
            else:
                #if an inactive account was used we are not logging them in
                return HttpResponse("Your Simplify account is disabled.")
        else:
            #bad login details were provided, so we can't log user in
            print(f"Invalid user details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")



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
        id=request.user.id
        #to show my courses
        studentUser= StudentProfile.objects.get(user=request.user)#getting the user
        studentCourse = studentUser.course.all()#getting the course for that user
        context_dict['myCourses']=studentCourse#passing it in the context dict
        
        course_name = Course.objects.all()
        context_dict['courses']=course_name
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
            tutor_profile=course_form.save(commit=False)
            tutor_profile.tutor= request.user
            course_form.save()
            return redirect(reverse('simplify_main_app:tutor-dashboard'))
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
            profileform.save(commit=False)
            id=request.user.id
            print(f'id of the user in the form:{id}')
            firstName= request.POST['firstname']
            lastName = request.POST['lastname']
            print(f'First Name in the form:{firstName}')
            print(f'Last Name in the form:{lastName}')
            u=User.objects.update_or_create(id=id,first_name=firstName,last_name=lastName)
            # u.first_name=p.firstname
            # u.last_name=p.lastname
            # print(u.first_name)
            # u.save()
            
            if request.user.role=='STD':
                
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

    

class AddMaterialView(View):
    def helper(self,course_name_slug):
        try:
            course = Course.objects.get(slug=course_name_slug)
        except Course.DoesNotExist:
            course=None
        return course

    @method_decorator(login_required)
    def get(self,request,course_name_slug):
        course=self.helper(course_name_slug)
        if course==None:
            return redirect('simplify_main_app/add_course.html')
        else:
            material_form =MaterialForm()
            context_dict={'form':material_form , 'course':course}
            return render(request, 'simplify_main_app/add_material.html', context_dict)

    @method_decorator(login_required)
    def post(self,request,course_name_slug):
        course = self.helper(course_name_slug)
        material_form = MaterialForm(request.POST)
        if material_form.is_valid():
            if course:
                courseMaterial = material_form.save(commit=False)
                courseMaterial.material=course
                courseMaterial.save()

                return redirect(reverse('simplify_main_app:course',kwargs={'course_name_slug':course_name_slug}))
        else:
            print(material_form.errors)
        return


class addCourseStudentView(View):
    def get(self,request,course_name_slug,course_id):
        user = request.user
        course = get_object_or_404(Course, id=course_id)
        Student_course = StudentProfile.objects.get_or_create(user=user)[0]
        # Check whether the Course is alread in StudentProfile or Not
        course_already_in_available = StudentProfile.objects.filter(course=course_id, user=user)
        if not  course_already_in_available:
            Student_course.course.add(course)
            Student_course.save()
        return redirect(reverse('simplify_main_app:student-dashboard'))