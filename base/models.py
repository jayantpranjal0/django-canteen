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

    def get_absolute_url(self):
        return reverse("organization_detail", kwargs={"slug": self.slug})

class Canteen(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    organization=models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Meal(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    price=models.IntegerField()
    canteen=models.ForeignKey(Canteen, on_delete=models.CASCADE)
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