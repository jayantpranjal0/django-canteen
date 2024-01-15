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
from django.shortcuts import redirect
from django.db.models import F


@login_required()
@customer_required()
def home(request):
    channel_layer = get_channel_layer()
    # check if the meals ordered by user are present which are not present but are prepared. if yes then display them on home page

    # user = User.objects.get(username='your_username')  # Replace 'your_username' with the actual username
    order_items = OrderItem.objects.filter(order__user=request.user, quantity_ordered__gt=F('quantity_delivered'))
    items={

    }
    if order_items:
        for order_item in order_items:
            prepared_items = Meal.get_prepared_items_by_canteen(order_item.meal.canteen)
            if order_item.meal in prepared_items:
                if prepared_items[order_item.meal] > order_item.quantity_delivered:
                    if(order_item.meal not in items):
                        items[order_item.meal]=0
                    items[order_item.meal]+=order_item.quantity_ordered-order_item.quantity_delivered
    
    if order_items:
        for order_item in order_items:
            prepared_items = Meal.get_prepared_items_by_canteen(order_item.meal.canteen)
            if order_item.meal in prepared_items:
                if prepared_items[order_item.meal] > order_item.quantity_delivered:
                    items[order_item.meal]=min(prepared_items[order_item.meal],items[order_item.meal])                    


    print(request.user)
    context = {"canteens": Canteen.all(),"items":items}
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
            return redirect('home')
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

@login_required()
@customer_required()
def customer(request):
    context={}

    if request.method=='POST':
        print(request.POST)
        if 'meal_name' in request.POST:
            meal_names=request.POST['meal_name']
            # convert meal names to list
            meal_names=meal_names.split(',')
            # print(meal_names,type(meal_names))
            amount=len(meal_names)
            for index in range(amount):
                meal=meal_names[index]
                print(index,meal)
                # order_with_meal=OrderItem.objects.filter(meal__name=meal,order__user=request.user, quantity_ordered__gt=F('quantity_delivered'))
                order_with_meal=OrderItem.objects.filter(meal__name=meal,order__user=request.user, quantity_ordered__gt=F('quantity_delivered'))
                count=request.POST['quantity']
                count=count.split(',')
                count=int(count[index])
                print(count)
                print(order_with_meal)
                for order in order_with_meal:
                    temp=min(order.quantity_ordered-order.quantity_delivered,int(count))
                    order.quantity_delivered+=temp
                    count-=temp
                    order.save()
                # also reduce the quantity of the meal in the canteen
                meal=Meal.objects.get(name=meal)
                meal.quantity-=count



            # meal=Meal.objects.get(name=meal_name)
            # if meal:
            #     order_items=OrderItem.objects.filter(meal=meal,order__user=request.user, quantity_ordered__gt=F('quantity_delivered'))
            #     if order_items:
            #         quantity=int(request.POST['quantity'])
            #         temp=0
                    
                    
            #         for order_item in order_items:
            #             if quantity>0:
            #                 temp+=min(quantity,order_item.quantity_ordered-temp)
            #                 order_item.quantity_delivered+=temp
            #                 quantity-=temp
            #                 order_item.save()
            #             else:
            #                 break
                            



                    
                    # order_item.save()
                    # if order_item.quantity_delivered>=order_item.quantity_ordered:
                    #     order_item.delete()
                #     return HttpResponse('Success')
                # else:
                #     return HttpResponse('Error')
        return HttpResponse('Success')
            # else:
            #     return HttpResponse('Error')

    return HttpResponse('Success')

    # return render(request, 'base/customer.html',context)










































































































































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






