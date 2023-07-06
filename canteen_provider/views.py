from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages


@login_required()
def providerPage(request, *args, **kwargs):
	context = {}
	return render(request, "canteen_provider/providerPage.html", context)
