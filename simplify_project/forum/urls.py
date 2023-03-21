from django.urls import path

from forum import views

urlpatterns = [
    path(r'forum/', views.forum, name='forum_f'),
    path(r'myaccount/', views.myaccount, name='forum_d'),
    path(r'creat_c/', views.creat_comment, name='forum_c'),



]