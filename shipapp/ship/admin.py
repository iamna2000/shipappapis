from django.contrib import admin
from .models import Category, Good, User, Place, Post
# Register your models here.

admin.site.register(Category)
admin.site.register(Good)
admin.site.register(Post)
admin.site.register(Place)
admin.site.register(User)
