from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('users', views.UserViewSet)
router.register('posts', views.PostViewSet)
router.register("goods", views.GoodViewSet, 'good')
router.register('places', views.PlaceViewSet, "place")
router.register('categories', views.CategoryViewSet, "category")

app_name = 'ship'
urlpatterns = [
    path('', include(router.urls)),
]
