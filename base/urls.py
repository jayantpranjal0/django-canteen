from django.contrib import admin
from django.urls import path, include
from base import views
from django.urls import path
from . import views


urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('',views.home,name='home'),
    path('canteen/<int:id>/',views.canteen,name='canteen'),
    path('canteen',views.canteen,name='canteen'),
    path('cart',views.cart,name='cart'),
    path('update_cart',views.update_cart,name='update_cart'),
]