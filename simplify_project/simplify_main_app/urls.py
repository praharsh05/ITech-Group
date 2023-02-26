from django.urls import path
from simplify_main_app import views

app_name='simplify_main_app'
urlpatterns= [
    path('', views.index, name='index'),
]