from django.contrib import admin
from .models import *


admin.site.register(User)
admin.site.register(Canteen)
admin.site.register(Meal)
admin.site.register(OrderItem)
admin.site.register(Order)