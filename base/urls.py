from django.contrib import admin
from django.urls import path, include
from base import views

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('',views.home,name='home'),
    path('canteen/<int:id>/',views.canteen,name='canteen'),
    path('canteen',views.canteen,name='canteen'),
]