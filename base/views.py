from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *



@login_required()
def home(request):
    favorite_canteens=[]
    favorite_meals=[]
    canteens=Canteens.objects.all()
    print(canteens)
    return render(request, 'base/home.html',params={'canteens':canteens,'favorite_canteens':favorite_canteens,'favorite_meals':favorite_meals})



# {% if user.is_authenticated %}
#                 {% comment %} {% if request.path == '/login/' or request.path == '/signup/' %}
#                     {% url 'home' %}
#                 {% endif %} {% endcomment %}
#                 Authenticated
#             {% else %}
#                 {% comment %} {% if request.path != '/login/' and request.path != '/signup/' %}
#                     {% url 'login' %}
#                 {% endif %} {% endcomment %}
#                 Not Authenticated
#             {% endif %} 


