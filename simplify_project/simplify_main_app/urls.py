from django.urls import path
from simplify_main_app import views

app_name='simplify_main_app'
urlpatterns= [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('forum/', views.forum, name='forum'),
]