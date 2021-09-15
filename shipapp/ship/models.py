from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')

class Category(models.Model):
    name = models.CharField(null=False, max_length=150, unique=True)

    def __str__(self):
        return self.name

class Good(models.Model):
    name = models.CharField(null=False, max_length=150)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='uploads/%Y/%m')

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=150, null=False)
    image = models.ImageField(upload_to='uploads/%Y/%m')
    content = models.TextField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    good = models.ForeignKey(Good, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Comment(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    content = models.TextField(null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Rating(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    rating = models.DecimalField(decimal_places=0, max_digits=5)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)