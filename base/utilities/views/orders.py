from .imports import *

@login_required()
@customer_required()
def orders(request):
    context={}
    return render(request, 'base/orders.html',context)