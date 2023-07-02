from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Canteen,Meal,User,Organization



@login_required()
def home(request):
    favorite_canteens=[]
    favorite_meals=[]
    canteens=Canteen.objects.all()
    print(canteens.count())
    return render(request, 'base/home.html',{'canteens':canteens,'favorite_canteens':favorite_canteens,'favorite_meals':favorite_meals})

@login_required()
def canteen(request,id):
    canteen=Canteen.objects.get(id=id)
    meals=Meal.objects.filter(canteen=canteen)
    return render(request, 'base/canteen.html',{'canteen':canteen,'meals':meals})

@login_required()
def meal(request,slug):
    meal=Meal.objects.get(slug=slug)
    return render(request, 'base/meal.html',{'meal':meal})


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


