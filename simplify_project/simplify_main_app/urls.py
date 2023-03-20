from django.urls import path
from simplify_main_app import views
from simplify_main_app.views import showCourseView, addCourseView, AddMaterialView

app_name='simplify_main_app'
urlpatterns= [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('student-dashboard/',views.student_dashboard, name='student-dashboard'),
    path('tutor-dashboard/', views.tutor_dashboard, name='tutor-dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('forum/', views.forum, name='forum'),
    path('course/<slug:course_name_slug>/', showCourseView.as_view(), name='course'),
    path('add_course/',addCourseView.as_view(),name='add_course'),
    path('course/<slug:course_name_slug>/add_material/',AddMaterialView.as_view(),name='add_material')
]