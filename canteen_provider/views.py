from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from base.custom_decorators import *

# @login_required()
# @canteen_provider_required()
def homePage(request, *args, **kwargs):

	print("homePage")
	
	context = {}
	# return HttpResponse("Under Construction")
	return render(request, 'canteen_provider/provider_page.html', context)
