from django.urls import path
from simplify_main_app import views
from simplify_main_app.views import showCourseView, addCourseView, AddMaterialView, ProfileView,addCourseStudentView
from simplify_main_app.views import IndexView, RegisterView, LoginView,LogoutView


app_name='simplify_main_app'
urlpatterns= [
    path('', IndexView.as_view(), name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('student-dashboard/',views.student_dashboard, name='student-dashboard'),
    path('tutor-dashboard/', views.tutor_dashboard, name='tutor-dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forum/', views.forum, name='forum'),
    path('course/<slug:course_name_slug>/', showCourseView.as_view(), name='course'),
    path('add_course/',addCourseView.as_view(),name='add_course'),
    path('course/<slug:course_name_slug>/add_material/',AddMaterialView.as_view(),name='add_material'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('course/<slug:course_name_slug>/<course_id>', addCourseStudentView.as_view(),name='add_course_student')
]