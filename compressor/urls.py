from django.contrib import admin
from django.urls import path
from compressor import views 

urlpatterns = [
    path('', views.index , name='index'),
    path('home', views.index , name='index'),
    path('compressor', views.index , name='index'),
    path('login', views.index , name='login'),
]