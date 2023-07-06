from django.urls import path , include
from .consumers import CanteenProvider

websocket_urlpatterns = [
	path("" , CanteenProvider.as_asgi()) ,
]
