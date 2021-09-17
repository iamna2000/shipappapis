from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('users', views.UserViewSet)

app_name = 'ship'
urlpatterns = [
    path('', include(router.urls)),
]
