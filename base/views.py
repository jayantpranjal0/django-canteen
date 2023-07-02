from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Canteen,Meal,User,Organization


@login_required()
def home(request):
    return render(request, 'base/home.html',{'canteens':Canteen.all(),})

@login_required()
def canteen(request,id):
    return render(request, 'base/canteen.html',{'canteen':Canteen.ID(id),'meals':Canteen.meals(id)})

@login_required()
def cart(request):
    return render(request, 'base/cart.html',{'cart':request.user.cart})



