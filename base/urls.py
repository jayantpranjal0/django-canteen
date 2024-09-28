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
    path('customer',views.customer,name='customer'),
    path('canteen_orders/<int:id>',views.canteen_orders,name='canteen_orders'),
    path('canteen/<int:id>/accept',views.customerPreparedItems,name='accept'),
    path('order_receive/<int:order_id>',views.orderReceive,name='order_receive_request_detail'),
    # path('canteen/<int:id>/otp_input',views.getOTPInput,name='otp_input'),
]