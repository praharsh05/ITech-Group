from django.urls import path
from simplify_main_app import views

app_name='simplify_main_app'
urlpatterns= [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('student-dashboard/',views.student_dashboard, name='student-dashboard'),
    path('tutor-dashboard/', views.tutor_dashboard, name='tutor-dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('forum/', views.forum, name='forum'),
    path('about-us/', views.aboutUs, name='about-us'),
    path('course/', views.course, name='course'),
]