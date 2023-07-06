from django.urls import path, include
from canteen_provider import views 
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
	# path("", chat_views.homePage, name="home-page"),
	# path("", chat_views.chatPage, name="chat-page"),
	path("",views.homePage, name="provider-home-page"),
	# path("")
	# path("auth/login/", LoginView.as_view( template_name="chat/LoginPage.html" ), name="login-user"),
	# path("auth/logout/", LogoutView.as_view(), name="logout-user"),
]
