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
    organizations=models.ManyToManyField('Organization', blank=True, related_name='users')
    date_joined = models.DateTimeField(auto_now_add=True)
    default_organization=models.ForeignKey('Organization', on_delete=models.CASCADE, blank=True, null=True)
    favourite_canteen=models.ManyToManyField('Organization', blank=True, related_name='+')
    cart=models.ForeignKey('Cart', on_delete=models.CASCADE, blank=True, null=True)
    favourite_meals=models.ManyToManyField('Meal', blank=True, related_name='+')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Organization(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100, unique=True, blank=True)
    description=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name
    # def getAbsolueteUrl(self):
    #     return reverse("organization_detail", kwargs={"slug": self.slug})
    def getCanteens(self):
        canteens=Canteen.objects.filter(organization=self)
        return canteens

class Canteen(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    organization=models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    # def get_orders(self):
    #     orders=Order.objects.filter(canteen=self)
    #     return orders
    def all():
        return Canteen.objects.all();
    def ID(id):
        return Canteen.objects.get(id=id)
    def meals(id):
        meals=Meal.objects.filter(canteen=Canteen.ID(id))
        return meals

class Meal(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    price=models.IntegerField()
    canteen=models.ForeignKey('Canteen', on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    items = models.ManyToManyField(Meal, through='CartItem', related_name='cart')
class CartItem(models.Model):
    cart=ForeignKey(Cart, on_delete=models.CASCADE)
    user=ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey('Meal', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'item')
        
class Order(models.Model):
    items=models.ManyToManyField(Meal,through='OrderItem',related_name='orders')
class OrderItem(models.Model):
    order=ForeignKey('Order',on_delete=models.CASCADE)
    user=ForeignKey(User,on_delete=models.CASCADE)
    item=models.ForeignKey('Meal',on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ( 'order', 'item')

class CompletedOrderHistory(models.Model):
    items=models.ManyToManyField(Meal,through='CompletedOrderHistoryItem',related_name='complete_order_history')
class CompletedOrderHistoryItem(models.Model):
    order=ForeignKey(CompletedOrderHistory,on_delete=models.CASCADE)
    user=ForeignKey(User,on_delete=models.CASCADE)
    item=models.ForeignKey(Meal,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ( 'order','item' )