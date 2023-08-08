from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate, login, logout
from base.models import *
from django.http import HttpResponse
from django.contrib import messages
from base.custom_decorators import *

@login_required()
# @canteen_provider_required()
def homePage(request, *args, **kwargs):
	# print(request.user)
	canteen=Canteen.objects.get(canteen_owner=request.user)
	# print(canteen)
	order_items=Order.getActiveOrdersItems(canteen)
	# print(order_items)
	context={
		'order_items':order_items,
	}
	return render(request, 'canteen_provider/live_code_feed.html', context)








# DEFINE A VERY GOOD SET OF RULES FOR DEBUUGING AND CONSOLE LOGGING AND TESTING





















# @login_required()
# @customer_required()
# def customer_orders():
# 	pass
