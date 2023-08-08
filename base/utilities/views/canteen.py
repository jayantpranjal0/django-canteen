from .imports import *


@login_required()
@customer_required()
def canteen(request,id):
    context={'canteen':Canteen.ID(id),'meals':Canteen.meals(id),"canteens":Canteen.all()}
    return render(request, 'base/canteen.html',context)
