from django.contrib import admin
from .models import Category, User, Place, Post, Comment
# Register your models here.

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Place)
admin.site.register(User)
admin.site.register(Comment)
