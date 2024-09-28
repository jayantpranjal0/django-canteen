from django.shortcuts import render, get_object_or_404
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
from django.utils.crypto import get_random_string


@login_required()
@customer_required()
def home(request):
    context = {
        "canteens": Canteen.all(),
    }
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
            # on order placeas only the canteen owner needs to be notified
            # Work requireed to be done here


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
    # Some correction adn explanation is required here too
    if request.method=='POST':
        print(request.POST)
        if 'meal_name' in request.POST:
            meal_names=request.POST['meal_name']
            meal_names=meal_names.split(',')
            amount=len(meal_names)
            for index in range(amount):
                meal=meal_names[index]
                print(index,meal)
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
                meal=Meal.objects.get(name=meal)
                meal.quantity-=count
        return HttpResponse('Success')

    return HttpResponse('Success')


def canteen_orders(request,id):
    # Make it work with order delivered and new addition
    channel_layer = get_channel_layer()

    canteen=Canteen.ID(id)
    
    order_items = OrderItem.objects.filter(order__user=request.user, quantity_ordered__gt=F('quantity_delivered'),meal__canteen=canteen)
    print(order_items)
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
    prepared_items = Meal.get_prepared_items_by_canteen(canteen)
    for meal in prepared_items:
        if meal not in items:
            items[meal]=0
        items[meal]=prepared_items[meal]                 
    

    print(request.user)
    print(items)
    context = {"canteens": Canteen.all(),"items":items}
    return render(request, 'base/collect_order.html', context)


def accept(request):
    # try:
    if request.method=='POST':
        # check otp
        otp=request.POST['otp']
        if 'meal_name' in request.POST:
            # get canteen from the meal
            canteen=Meal.objects.get(name=request.POST['meal_name']).canteen
            if(canteen.otp!=otp):
                return HttpResponse('Error')
            

            meal_names=request.POST['meal_name']
            meal_names=meal_names.split(',')
            amount=len(meal_names)
            for index in range(amount):
                meal=meal_names[index]
                print(index,meal)
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
                meal=Meal.objects.get(name=meal)
                meal.qunatity_prepared-=count

                meal.save()
    return redirect('home')

from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.crypto import get_random_string
from .models import OrderReceiveRequest, ReceivedItem, Meal, Canteen

def customerPreparedItems(request, id):
    # Handle GET request
    if request.method == 'GET':
        canteen = Canteen.objects.get(id=id)
        order_items = OrderItem.objects.filter(
            order__user=request.user,
            quantity_ordered__gt=F('quantity_delivered'),
            meal__canteen=canteen
        )
        items = {}
        if order_items:
            for order_item in order_items:
                prepared_items = Meal.get_prepared_items_by_canteen(order_item.meal.canteen)
                if order_item.meal in prepared_items:
                    if prepared_items[order_item.meal] > order_item.quantity_delivered:
                        if order_item.meal not in items:
                            items[order_item.meal] = 0
                        items[order_item.meal] += order_item.quantity_ordered - order_item.quantity_delivered

        prepared_items = Meal.get_prepared_items_by_canteen(canteen)
        for meal in prepared_items:
            if meal not in items:
                items[meal] = 0
            items[meal] = prepared_items[meal]

        context = {
            "canteens": Canteen.objects.all(),
            "items": items,
            'id': canteen.id
        }
        
        return render(request, 'base/customer_prepared_items.html', context)
    
    # Handle POST request
    elif request.method == 'POST':
        canteen = Canteen.objects.get(id=id)
        
        # Check if all quantities are zero
        all_zero = True
        for key, value in request.POST.items():
            if key.startswith('quantity_') and int(value) > 0:
                all_zero = False
                break
        
        # If all items are zero, return an error response
        if all_zero:
            return HttpResponse("Error: No items selected. Please select at least one item.", status=400)
        
        # Create a new OrderReceiveRequest instance if quantities are valid
        order_request = OrderReceiveRequest.objects.create(
            canteen=canteen,
            otp=get_random_string(length=4, allowed_chars='0123456789')  # Generating a random OTP
        )
        
        # Loop through the POST data and create ReceivedItem instances
        for key, value in request.POST.items():
            if key.startswith('quantity_') and int(value) > 0:
                meal_name = key.replace('quantity_', '')
                meal = Meal.objects.get(name=meal_name)
                
                # Create a ReceivedItem for each meal that has a quantity > 0
                received_item = ReceivedItem.objects.create(
                    meal=meal,
                    quantity_received=value
                )
                
                # Associate the ReceivedItem with the OrderReceiveRequest
                order_request.receivedItems.add(received_item)
        
        # Redirect to the page of the newly created OrderReceiveRequest
        return redirect('order_receive_request_detail', order_id=order_request.id)


def orderReceive(request, order_id):
    # Fetch the OrderReceiveRequest using get_object_or_404 for better error handling
    order_request = get_object_or_404(OrderReceiveRequest, id=order_id)

    if request.method == 'GET':
        # Pass the order_request to the context
        context = {
            'order_request': order_request
        }

        # Render the template with the order_request context
        return render(request, 'base/order_receive_request_detail.html', context)



def getOTPInput(request,id):
    if request.method == 'GET':
        return render(request, 'base/otp_input.html')
    elif request.method == 'POST':
        print(request.POST)
