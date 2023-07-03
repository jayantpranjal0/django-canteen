from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateTimeField, IntegerField, TextField
from django.db.models.fields.related import ForeignKey
from django.urls import reverse
from django.utils.text import slugify


class User(AbstractUser):
    username = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    full_name=models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    default_canteen=models.ForeignKey('Canteen', on_delete=models.CASCADE, blank=True, null=True)
    favourite_canteen=models.ManyToManyField('Canteen', blank=True, related_name='+')
    favourite_meals=models.ManyToManyField('Meal', blank=True, related_name='+')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Canteen(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    def getOrders(self):
        orders=Order.objects.filter(canteen=self)
        return orders
    def getOrderHistory(self):
        orders=CompletedOrderHistory.objects.filter(canteen=self)
        return orders
    def all():
        return Canteen.objects.all();
    def ID(id):
        return Canteen.objects.get(id=id)
    def meals(id):
        meals=Meal.objects.filter(canteen=Canteen.ID(id))
        return meals
    def meals(self):
        meals=Meal.objects.filter(canteen=self)
        return meals
    # def getCurrentOrders():
    # def getPendingItems():
        

class Meal(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    price=models.IntegerField()
    canteen=models.ForeignKey('Canteen', on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    meal=models.ForeignKey('Meal', on_delete=models.CASCADE)
    quantity_ordered=models.PositiveIntegerField()
    quantity_delivered=models.PositiveIntegerField(blank=True, null=True)
    order=models.ForeignKey('Order', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name_plural='OrdersItems'
        unique_together=('meal','order')

class Order(models.Model):
    time_added=models.DateTimeField(auto_now_add=True)
    time_completed=models.DateTimeField(blank=True, null=True)
    user=models.ForeignKey('User', on_delete=models.CASCADE)
    items=models.ManyToManyField('Meal', through=OrderItem)

    def __str__(self):
        return str(self.id)
    def getItems(self):
        items=OrdersItem.objects.filter(order=self)
        return items
    def getItemsCount(self):
        items=OrdersItem.objects.filter(order=self)
        return items.count()
    def getItemsTotal(self):
        items=OrdersItem.objects.filter(order=self)
        total=0
        for item in items:
            total+=item.meal.price*item.quantity
        return total
    def activeOrders():
        return Order.objects.filter(time_completed=None)
    def completedOrders():
        return Order.objects.filter(time_completed__isnull=False)
    def getActiveOrders(canteen):
        return Order.objects.filter(time_completed=None,canteen=canteen)
    def getCompletedOrders(canteen):
        return Order.objects.filter(time_completed__isnull=False,canteen=canteen)
    # Item wise order count bhi krna tha

    # def getItemOrdersCount(canteen):
    #     items=OrderItem.objects.filter(order__canteen=canteen)
    #     return items.count()


