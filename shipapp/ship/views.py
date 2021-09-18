from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics
from rest_framework.parsers import MultiPartParser
from .models import Category, Good, Post, User, Place
from .serializers import CategorySerializer, GoodSerializer, PostSerializer, PlaceSerializer, UserSerializer
from .paginator import BasePaginator

# Create your views here.

class UserViewSet(viewsets.ViewSet,
                  generics.ListAPIView,
                  generics.CreateAPIView,
                  generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated]

        return [permissions.AllowAny]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(active=True)
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]

class GoodViewSet(viewsets.ModelViewSet):
    queryset = Good.objects.filter(active=True)
    serializer_class = GoodSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]

class PlaceViewSet(viewsets.ModelViewSet,
                      generics.ListAPIView):
    serializer_class = PlaceSerializer
    pagination_class = BasePaginator

    def get_queryset(self):
        # places = Place.objects.filter(active = True)
        places = Place.objects.all()

        q = self.request.query_params.get('q')
        if q is not None:
            places = places.filter(name__icontains=q)

        return places

class CategoryViewSet(viewsets.ModelViewSet,
                      generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

def index(request):
    return render(request, template_name='index.html', context={
        'name' : 'Trọng Hảo'
    })