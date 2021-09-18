from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')

class Category(models.Model):
    name = models.CharField(null=False, max_length=150, unique=True)

    def __str__(self):
        return self.name

class ModelBase(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Good(ModelBase):
    class Meta :
        ordering = ["-id"]
    name = models.CharField(null=False, max_length=150)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='goods/%Y/%m')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Post(ModelBase):
    title = models.CharField(max_length=150, null=False)
    image = models.ImageField(upload_to='uploads/%Y/%m')
    content = models.TextField(null=False, blank=False)
    completed = models.BooleanField(default=False)
    receipt_point = models.ManyToManyField('Place', related_name="receipt_point", blank=False, null=False)
    delivery_point = models.ManyToManyField('Place', related_name="delivery_point", blank=False, null=False)
    good = models.ForeignKey(Good, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username + " --> " + self.good.name

class Comment(ModelBase):
    content = models.TextField(null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    shipper = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Rating(models.Model):
    rating = models.DecimalField(decimal_places=0, max_digits=5)
    shipper = models.ForeignKey(User, related_name="shipper", on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE, null=True)

class Place(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name