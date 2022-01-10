from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')
    is_staff = models.BooleanField(default=False)

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


class Post(ModelBase):
    class Meta :
        ordering = ["-id"]
    title = models.CharField(max_length=150, null=True)
    image = models.ImageField(upload_to='uploads/%Y/%m')
    content = models.TextField(null=False, blank=False)
    completed = models.BooleanField(default=False)
    receipt_point = models.ForeignKey('Place', related_name="from_id", on_delete=models.CASCADE, null=True)
    delivery_point = models.ForeignKey('Place', related_name="to_id", on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content

class Comment(ModelBase):
    content = models.TextField(null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    shipper = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content

class CommentShipper(ModelBase):
    content = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, related_name="user_id", on_delete=models.CASCADE, null=True)
    shipper = models.ForeignKey(User, related_name="shipper_id", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content

class Place(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class PostView(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    post = models.OneToOneField(Post, on_delete=models.CASCADE)

class Rating(models.Model):
    rating = models.DecimalField(decimal_places=0, max_digits=5)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    shipper = models.ForeignKey(User, related_name="shipper", on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE, null=True)

