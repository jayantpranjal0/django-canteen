from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
import json
from base.custom_decorators import *
from canteen_provider.consumers import CanteenProvider, CustomerConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from base.utilities.customer import *

@login_required()
@customer_required()
def home(request):
    context = {"canteens": Canteen.all()}
    channel_layer = get_channel_layer()
    return render(request, 'base/home_page.html', context)














@login_required()
@customer_required()
def canteen(request,id):
    context={'canteen':Canteen.ID(id),'meals':Canteen.meals(id),"canteens":Canteen.all()}
    return render(request, 'base/canteen.html',context)

@login_required()
@customer_required()
def checkout(request):
    try:
        if request.method=='POST':
            # print(request.POST['order'])
            order=request.POST['order']
            orderRequest=json.loads(order)
            order=Order.objects.create(
                user=request.user,
            )
            for meal,quantity in orderRequest.items():
                if quantity>0:
                    meal = Meal.objects.get(id=meal)
                    if meal!=None:
                        temp = OrderItem.objects.create(
                            order=order,
                            meal=meal,
                            quantity_ordered=quantity,
                            quantity_delivered=0,

                        )
                    else:
                        return HttpResponse('Error')
            sendOrder(order)
            return HttpResponse('Success')
        else:
            return HttpResponse('Error')
    except Exception as e:
        print(e)
        return HttpResponse('Error')

























@login_required()
@customer_required()
def orders(request):
    context={}
    return render(request, 'base/orders.html',context)










































































































































# from base.utilities.views.views import *
# @login_required()
# @customer_required()
# def home(request):
#     context = {"canteens": Canteen.all()}
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         'jayant_pranjal',
#         {
#             'type': 'custom_message_handler',
#             'text': json.dumps({
#                 "message": "Test Message",
#             })
#         }
#     )
#     return render(request, 'base/home_page.html', context)


# @login_required()
# @customer_required()
# def canteen(request,id):
#     context={'canteen':Canteen.ID(id),'meals':Canteen.meals(id),"canteens":Canteen.all()}
#     return render(request, 'base/canteen.html',context)

# @login_required()
# @customer_required()
# def checkout(request):
#     try:
#         if request.method=='POST':
#             print(request.POST['order'])
#             order=request.POST['order']
#             orderRequest=json.loads(order)
#             order=Order.objects.create(
#                 user=request.user,
#             )
#             for meal,quantity in orderRequest.items():
#                 print(meal,quantity)
#                 if quantity>0:
#                     meal=Meal.objects.get(id=meal)
#                     if meal!=None:
#                         OrderItem.objects.create(
#                             order=order,
#                             meal=meal,
#                             quantity_ordered=quantity
#                         )
#                     else:
#                         return HttpResponse('Error')
#             print("Tried")
#             print(orderRequest)
#             CanteenProvider.sendOrder(order=orderRequest)
#             print("Done")
#             return HttpResponse('Success')
#             # CanteenProvider.sendMessage(orderRequest)
#         else:
#             return HttpResponse('Error')
#     except Exception as e:
#         print(e)
#         return HttpResponse('Error')


# @login_required()
# @customer_required()
# def orders(request):
#     context={}
#     return render(request, 'base/orders.html',context)






