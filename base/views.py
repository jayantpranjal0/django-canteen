from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
import json
from base.custom_decorators import *

@login_required()
@customer_required()
def home(request):
    return HttpResponse('Under Construction')

@login_required()
@customer_required()
def canteen(request,id):
    return render(request, 'base/canteen.html',{'canteen':Canteen.ID(id),'meals':Canteen.meals(id),"canteens":Canteen.all()})

@login_required()
@customer_required()
def checkout(request):
    try:
        if request.method=='POST':
            print(request.POST['order'])
            order=request.POST['order']
            orderRequest=json.loads(order)
            order=Order.objects.create(
                user=request.user,
            )
            for meal,quantity in orderRequest.items():
                print(meal,quantity)
                if quantity>0:
                    meal=Meal.objects.get(id=meal)
                    if meal!=None:
                        OrderItem.objects.create(
                            order=order,
                            meal=meal,
                            quantity_ordered=quantity
                        )
                    else:
                        return HttpResponse('Error')
            return HttpResponse('Success')
        else:
            return HttpResponse('Error')
    except Exception as e:
        print(e)
        return HttpResponse('Error')