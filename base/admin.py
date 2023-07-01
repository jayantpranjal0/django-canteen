from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Organization)
admin.site.register(Canteen)
admin.site.register(Meal)
admin.site.register(Order)
# admin.site.register(Payment)

