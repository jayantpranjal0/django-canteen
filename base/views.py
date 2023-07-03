from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Canteen,Meal,User,Organization
import json

@login_required()
def home(request):
    return render(request, 'base/home.html',{'canteens':Canteen.all(),})

@login_required()
def canteen(request,id):
    return render(request, 'base/canteen.html',{'canteen':Canteen.ID(id),'meals':Canteen.meals(id)})

@login_required()
def cart(request):
    cart=User.objects.get(id=request.user.id).cartItems()
    # print(cart['cart_items'])
    return render(request, 'base/cart.html',cart)

@login_required()
def update_cart(request):
    if request.method=='POST':
        # redirect_url=request.POST['redirect_url']
        pass

    pass




