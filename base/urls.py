from django.contrib import admin
from django.urls import path, include
from base import views

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('',views.home,name='home'),
]