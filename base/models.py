from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateTimeField, IntegerField, TextField
from django.db.models.fields.related import ForeignKey
# from django.utils import timezone
# from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.

# Use django groups instead of organizations
# User Model
class User(AbstractBaseUser):
    # username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    # phone_number=models.PhoneNumberField(_("phone number"), blank=True)
    # profile_picture=models.ImageField(upload_to='profile_pictures/', blank=True)
    full_name=models.CharField(max_length=100, blank=True)
    organizations=models.ManyToManyField('Organization', blank=True, related_name='users')
    date_joined = models.DateTimeField(auto_now_add=True)
    default_organization=models.ForeignKey('Organization', on_delete=models.CASCADE, blank=True, null=True)
    favourite_canteen=models.ManyToManyField('Organization', blank=True, related_name='+')
    favourite_meals=models.ManyToManyField('Meal', blank=True, related_name='+')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email






# Model For Organization
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

    def get_absolute_url(self):
        return reverse("organization_detail", kwargs={"slug": self.slug})


# Model For Canteen
# Future Work: Maybe add a field for the location of the canteen and allow one canteen to have multiple locations and multiple organizations
class Canteen(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    organization=models.ForeignKey(Organization, on_delete=models.CASCADE)
    meals=models.ManyToManyField('Meal', blank=True, related_name='canteens')
    # Make this thing a little easier to use (Meals not always same and even if same it can get messy sometimes)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Model For Meal
class Meal(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    price=models.IntegerField()
    # canteen=models.ForeignKey(Canteen, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name




class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    meal=models.ForeignKey(Meal, on_delete=models.CASCADE)
    canteen=models.ForeignKey(Canteen, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    status=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.meal.name

# class Payment(models.Model):
#     order=models.ForeignKey(Order, on_delete=models.CASCADE)
#     amount=models.IntegerField()
#     payment_method=models.CharField(max_length=100)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.order.meal.name

# class Delivery(models.Model):
#     order=models.ForeignKey(Order, on_delete=models.CASCADE)
#     delivery_address=models.TextField()
#     delivery_time=models.DateTimeField()
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.order.meal.name

# class Review(models.Model):
#     user=models.ForeignKey(User, on_delete=models.CASCADE)
#     meal=models.ForeignKey(Meal, on_delete=models.CASCADE)
#     review=models.TextField()
#     rating=models.IntegerField()
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.meal.name

# class Cart(models.Model):
#     user=models.ForeignKey(User, on_delete=models.CASCADE)
#     meal=models.ForeignKey(Meal, on_delete=models.CASCADE)
#     quantity=models.IntegerField()
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.meal.name

# class Favorite(models.Model):
#     user=models.ForeignKey(User, on_delete=models.CASCADE)
#     meal=models.ForeignKey(Meal, on_delete=models.CASCADE)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.meal.name

# class Notification(models.Model):
#     user=models.ForeignKey(User, on_delete=models.CASCADE)
#     message=models.TextField()
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.message

# class Contact(models.Model):
#     name=models.CharField(max_length=100)
#     email=models.EmailField(max_length=100)
#     # phone_number=models.PhoneNumberField(_("phone number"), blank=True)
#     message=models.TextField()
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

# class About(models.Model):
#     title=models.CharField(max_length=100)
#     description=models.TextField()
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title

# class Faq(models.Model):
#     question=models.CharField(max_length=100)
#     answer=models.TextField()
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.question

# class Terms(models.Model):
#     title=models.CharField(max_length=100)
#     description=models.TextField()
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title

# class Privacy(models.Model):
#     title=models.CharField(max_length=100)
#     description=models.TextField()
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title

# class Social(models.Model):
#     name=models.CharField(max_length=100)
#     icon=models.CharField(max_length=100)
#     link=models.URLField(max_length=100)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

# class Setting(models.Model):
#     name=models.CharField(max_length=100)
#     logo=models.ImageField(upload_to="logo")
#     favicon=models.ImageField(upload_to="favicon")
#     address=models.TextField()
#     # phone_number=models.PhoneNumberField(_("phone number"), blank=True)
#     email=models.EmailField(max_length=100)
#     facebook=models.URLField(max_length=100)
#     twitter=models.URLField(max_length=100)
#     instagram=models.URLField(max_length=100)
#     youtube=models.URLField(max_length=100)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

# class Slider(models.Model):
#     title=models.CharField(max_length=100)
#     description=models.TextField()
#     image=models.ImageField(upload_to="slider")
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title

# class Chef(models.Model):
#     name=models.CharField(max_length=100)
#     designation=models.CharField(max_length=100)
#     image=models.ImageField(upload_to="chef")
#     facebook=models.URLField(max_length=100)
#     twitter=models.URLField(max_length=100)
#     instagram=models.URLField(max_length=100)
#     youtube=models.URLField(max_length=100)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

# class Category(models.Model):
#     name=models.CharField(max_length=100)
#     image=models.ImageField(upload_to="category")
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name