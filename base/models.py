from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateTimeField, IntegerField, TextField
from django.db.models.fields.related import ForeignKey
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import F
from collections import defaultdict




class User(AbstractUser):
    username = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    full_name=models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Canteen(models.Model):
    canteen_owner=models.ForeignKey('User', on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    otp=models.CharField(max_length=4, blank=True)

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

class Profile(models.Model):
    user=models.OneToOneField('User', on_delete=models.CASCADE)
    bio=models.TextField(blank=True)
    birth_date=models.DateField(null=True, blank=True)
    default_canteen=models.ForeignKey('Canteen', on_delete=models.CASCADE, blank=True, null=True)
    favourite_canteen=models.ManyToManyField('Canteen', blank=True, related_name='+')
    favourite_meals=models.ManyToManyField('Meal', blank=True, related_name='+')

    def __str__(self):
        return self.user.username


class Provider(models.Model):
    user=models.OneToOneField('User', on_delete=models.CASCADE)
    canteen=models.ForeignKey('Canteen', on_delete=models.CASCADE)
    bio=models.TextField(blank=True)
    birth_date=models.DateField(null=True, blank=True)
    pass

class Meal(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    price=models.IntegerField()
    canteen=models.ForeignKey('Canteen', on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    qunatity_prepared=models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    def get_prepared_items():
        # Get prepared quantity for each meal in the specific canteen
        prepared_items = defaultdict(int)
        order_items = OrderItem.objects.filter(quantity_delivered__gt=0)
        for order_item in order_items:
            prepared_items[order_item.meal] += order_item.quantity_delivered
        return prepared_items
    
        # return order_items
    def get_prepared_items_by_canteen(canteen):
        # Get prepared quantity for each meal in the specific canteen
        prepared_items = defaultdict(int)
        meals = Meal.objects.filter(qunatity_prepared__gt=0,canteen=canteen)
        for meal in meals:
            prepared_items[meal.name] += meal.qunatity_prepared
        return prepared_items


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
    @property
    def items_to_be_delivered(self):
        return self.quantity_ordered - (self.quantity_delivered or 0)

class Order(models.Model):
    time_added=models.DateTimeField(auto_now_add=True)
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

    def getActiveOrdersItems(canteen):
        orderitems = OrderItem.objects.filter(quantity_ordered__gt=F('quantity_delivered'),meal__canteen=canteen)
        return orderitems

    def getCompletedOrders(canteen):
        return Order.objects.filter(time_completed__isnull=False,canteen=canteen)

    def get_items_to_be_delivered(self):
        items_to_be_delivered = defaultdict(int)
        order_items = OrderItem.objects.filter(meal__canteen=self, quantity_delivered__lt=F('quantity_ordered'))

        for order_item in order_items:
            items_to_be_delivered[order_item.meal] += order_item.quantity_ordered - (order_item.quantity_delivered or 0)
        #     print(order_item.meal,":",items_to_be_delivered[order_item.meal])
        # print(items_to_be_delivered)

        return items_to_be_delivered

