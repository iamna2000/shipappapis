from typing import Union

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Post, User, Place, Comment, Rating, PostView
from .serializers import CategorySerializer, \
    PostSerializer, \
    PlaceSerializer, \
    UserSerializer, \
    CommentSerializer, \
    RatingSerializer, \
    PostViewSerializer, \
    CommentShipper, \
    ShipperViewSerializer, \
    CommentShipperSerializer
from .paginator import BasePaginator
from django.conf import settings
from django.db.models import F

# Create your views here.

# class UserViewSet(viewsets.ViewSet,
#                   generics.ListAPIView,
#                   generics.CreateAPIView,
#                   generics.RetrieveAPIView,
#                   generics.UpdateAPIView):
#     queryset = User.objects.filter(is_active=True)
#     serializer_class = UserSerializer
#     parser_classes = [MultiPartParser, ]
#
#     def get_permissions(self):
#         if self.action == 'retrieve':
#             return [permissions.IsAuthenticated()]
#
#         return [permissions.AllowAny()]
#
#     @action(methods=['get'], detail=False, url_path="current-user")
#     def get_current_user(self, request):
#         return Response(self.serializer_class(request.user).data, status=status.HTTP_200_OK)
class UserViewSet(viewsets.ViewSet,
                  generics.ListAPIView,
                  generics.RetrieveAPIView,
                  generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action in ['get_current_user', 'retrieve']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False, url_path="current-user")
    def get_current_user(self, request):
        return Response(self.serializer_class(request.user, context={"request": request}).data,
                        status=status.HTTP_200_OK)

    # @action(methods=['get'], detail=False, url_path="shippers")
    # def get_shipper(self, request):
    #     s=User.objects.values("username","email","first_name", "last_name", "date_joined", "is_staff")
    #
    #     print(s)
    #     return Response(ShipperViewSerializer(s).data,
    #                     status=status.HTTP_200_OK)

    def get_queryset(self):

        s = User.objects.filter(is_staff=True)
        return s

    @action(methods=['post'], detail=True, url_path='rating')
    def rate(self, request, pk):
        try:
            rating = int(request.data['rating'])
        except Union[IndexError, ValueError]:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            r = Rating.objects.update_or_create(user=request.user,
                                                shipper=self.get_object(),
                                                defaults={"rating": rating})

            return Response(RatingSerializer(r).data,
                            status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path="add-comment")
    def add_comment(self, request, pk):
        content = request.data.get('content')
        if content:
            c = CommentShipper.objects.create(content=content,
                                       shipper=self.get_object(),
                                       user=request.user)

            return Response(CommentShipper(c, context={"request": request}).data,
                            status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, url_path="comments")
    def get_comments(self, request, pk):
        c = self.get_object()
        return Response(
            CommentShipperSerializer(c.comment_set.order_by("-id").all(), many=True, context={"request": self.request}).data,
            status=status.HTTP_200_OK)

class AuthInfo(APIView) :
    def get(self, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)

class CategoryViewSet(viewsets.ViewSet,
                      generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PostViewSet(viewsets.ViewSet,
                  generics.ListAPIView,
                  generics.RetrieveAPIView):
    pagination_class = BasePaginator
    serializer_class = PostSerializer


    def get_queryset(self):
        posts = Post.objects.filter(active=True)

        q = self.request.query_params.get('q')
        if q is not None:
            posts = posts.filter(content__icontains=q)

        cate_id = self.request.query_params.get('category_id')
        if cate_id is not None:
            posts = posts.filter(category_id=cate_id)

        return posts


    def get_permissions(self):
        if self.action in ['add_comment','add_post']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['post'], detail=False ,url_path="add-post")
    def add_post(self, request):
        if request.user.is_staff == False:
            content = request.data['content']
            image = request.FILES.get('image')
            receipt_point = request.data['receipt_point']
            delivery_point = request.data['delivery_point']
            category = request.data['category']
            if image is not None:
                post = Post.objects.create(content = content,
                                           image = image,
                                           receipt_point = Place.objects.get(id=receipt_point) ,
                                           delivery_point = Place.objects.get(id=delivery_point) ,
                                           category = Category.objects.get(id=category),
                                           user=request.user
                                           )
                post.save()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        else:
         return Response(status=status.HTTP_403_FORBIDDEN)

    @action(methods=['post'], detail=True, url_path="add-comment")
    def add_comment(self, request, pk):
        if request.user.is_staff == True:
            content = request.data.get('content')
            if content:
                c = Comment.objects.create(content=content,
                                            post=self.get_object(),
                                            shipper=request.user)

                return Response(CommentSerializer(c, context={"request": request}).data,
                                status=status.HTTP_201_CREATED)

            return Response(status = status.HTTP_400_BAD_REQUEST)

        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    @action(methods=['get'], detail=True, url_path="comments")
    def get_comments(self, request, pk):
        c = self.get_object()
        return Response(
            CommentSerializer(c.comment_set.order_by("-id").all(), many=True, context={"request": self.request}).data,
            status=status.HTTP_200_OK)



    @action(methods=['get'], detail=True, url_path='views')
    def inc_view(self, request, pk):
        v, created = PostView.objects.get_or_create(post=self.get_object())
        v.views = F('views') + 1
        v.save()

        v.refresh_from_db()

        return Response(PostViewSerializer(v).data, status=status.HTTP_200_OK)

class PlaceViewSet(viewsets.ViewSet,
                      generics.ListAPIView):
    serializer_class = PlaceSerializer

    def get_queryset(self):
        # places = Place.objects.filter(active = True)
        places = Place.objects.all()

        q = self.request.query_params.get('q')
        if q is not None:
            places = places.filter(name__icontains=q)

        return places

class CommentViewSet(viewsets.ViewSet,
                     generics.DestroyAPIView,
                     generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]


    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().shipper:
            return super().destroy(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        if request.user == self.get_object().shipper:
            return super().partial_update(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)
