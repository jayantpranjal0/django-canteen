from django.contrib import admin
from django.urls import path, include
from base import views
from django.urls import path
from . import views


urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('',views.home,name='home'),
    path('canteen/<int:id>/',views.canteen,name='canteen'),
    path('checkout',views.checkout,name='checkout'),
    path('orders',views.orders,name='customer_orders'),
]