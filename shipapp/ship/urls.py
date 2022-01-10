from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register("users", views.UserViewSet, 'user')
router.register("posts", views.PostViewSet, 'post')
router.register("places", views.PlaceViewSet, 'place')
router.register("categories", views.CategoryViewSet, 'category')
router.register("comments", views.CommentViewSet, 'comment')

urlpatterns = [
    path('', include(router.urls)),
    path('oauth2_info/', views.AuthInfo.as_view())
]
