from django.urls import path
from simplify_main_app import views
from simplify_main_app.views import showCourseView, addCourseView, AddMaterialView, ProfileView,addCourseStudentView
from simplify_main_app.views import IndexView, RegisterView, LoginView,LogoutView,StudentDashboardView
from simplify_main_app.views import TutorDashboardView


app_name='simplify_main_app'
urlpatterns= [
    path('', IndexView.as_view(), name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('student_dashboard/',StudentDashboardView.as_view(), name='student-dashboard'),
    path('tutor_dashboard/', TutorDashboardView.as_view(), name='tutor-dashboard'),
    path('course/<slug:course_name_slug>/', showCourseView.as_view(), name='course'),
    path('add_course/',addCourseView.as_view(),name='add_course'),
    path('course/<slug:course_name_slug>/add_material/',AddMaterialView.as_view(),name='add_material'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('course/<slug:course_name_slug>/<course_id>', addCourseStudentView.as_view(),name='add_course_student'),
    path('forum/', views.forum, name='forum'),
    path('about-us/', views.aboutUs, name='about-us'),
    path('course/', views.course, name='course'),
    path('addCourse/', views.addCourse, name='add-course'),
]