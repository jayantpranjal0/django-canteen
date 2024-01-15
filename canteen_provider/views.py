from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate, login, logout
from base.models import *
from django.http import HttpResponse
from django.contrib import messages
from base.custom_decorators import *
import json

@login_required()
# @canteen_provider_required()
def homePage(request, *args, **kwargs):
	# canteen=Canteen.objects.get(canteen_owner=request.user)
	order_items=Order.get_items_to_be_delivered(canteen)
	prepared_items=Meal.get_prepared_items_by_canteen()
	
	items={
	}
	for i,j in order_items.items():
		items[str(i)]=j
	print(items)
	context= { 'order_items':items}
	return render(request, 'canteen_provider/provider_page.html', context)
