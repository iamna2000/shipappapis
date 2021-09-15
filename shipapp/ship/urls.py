from django.urls import path
from . import views

app_name = 'ship'
urlpatterns = [
    path('', views.index, name="index"),
]
