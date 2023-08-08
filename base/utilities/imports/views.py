from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from base.models import *
import json
from base.custom_decorators import *
from canteen_provider.consumers import CanteenProvider, CustomerConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json