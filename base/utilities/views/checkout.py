from .imports import *


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
            print("Tried")
            print(orderRequest)
            CanteenProvider.sendOrder(order=orderRequest)
            print("Done")
            return HttpResponse('Success')
            # CanteenProvider.sendMessage(orderRequest)
        else:
            return HttpResponse('Error')
    except Exception as e:
        print(e)
        return HttpResponse('Error')
