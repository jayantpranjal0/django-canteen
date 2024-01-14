from django.urls import path , include
from .consumers import CanteenProvider,CustomerConsumer

websocket_urlpatterns = [
	path("" , CanteenProvider.as_asgi()) ,
    path('customer',CustomerConsumer.as_asgi()),
]
