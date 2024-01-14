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
	canteen=Canteen.objects.get(canteen_owner=request.user)
	order_items=Order.get_items_to_be_delivered(canteen)
	prepared_items=Meal.get_prepared_items_by_canteen(canteen)

	items={
	}

	for i,j in order_items.items():
		items[str(i)]=j
		# items[str(i)]={
		# 	'items_count':j,
		# 	'prepared':0
		# }

	# for i,j in prepared_items.items():
		# items[str(i)]=items.get(str(i),0)+j
		# items[str(i)]={
		# 	'prepared':j,
		# 	'delivered':items.get(str(i),0)
		# }
		# left shift 15 times before adding the prepared items

		# items[str(i)]={
		# 	'item':items.get(str(i))['items_count'],
		# 	'prepared':j,
		# }


	print(items)
	context= { 'order_items':items}
	return render(request, 'canteen_provider/provider_page.html', context)








# DEFINE A VERY GOOD SET OF RULES FOR DEBUUGING AND CONSOLE LOGGING AND TESTING





















# @login_required()
# @customer_required()
# def customer_orders():
# 	pass
