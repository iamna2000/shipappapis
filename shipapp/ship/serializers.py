from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Category, Post, Place, User, Comment, Rating, PostView, CommentShipper


class UserSerializer(ModelSerializer):
    avatar = SerializerMethodField()

    def get_avatar(self, user):
        request = self.context['request']
        if user.avatar:
            name = user.avatar.name
            if name.startswith("static/"):
                path = '/%s' % name
            else:
                path = '/static/%s' % name

            return request.build_absolute_uri(path)

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email","date_joined","password", "username", "avatar"]
        extra_kwargs = {
            'password' : {'write_only' : 'true'}
        }


class PlaceSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class PostSerializer(ModelSerializer):

    image = SerializerMethodField()
    user = UserSerializer()
    delivery_point = PlaceSerializer()
    receipt_point = PlaceSerializer()

    def get_image(self, post):
        request = self.context['request']
        name = post.image.name
        if name.startswith("static/"):
            path = '/%s' % name
        else:
            path = '/static/%s' % name

        return request.build_absolute_uri(path)


    class Meta:
        model = Post
        fields = ["id", "title", "image", "created_date", "content", "delivery_point", "category", "receipt_point", "user" ]


class CommentSerializer(ModelSerializer):
    shipper = SerializerMethodField()

    def get_shipper(self, comment):
        return UserSerializer(comment.shipper, context={"request": self.context.get('request')}).data

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_date', 'shipper']

class CommentShipperSerializer(ModelSerializer):
    user = SerializerMethodField()

    def get_user(self, comment):
        return UserSerializer(comment.user, context={"request": self.context.get('request')}).data

    class Meta:
        model = CommentShipper
        fields = ['id', 'content', 'created_date', 'user']

class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "rating", "created_date"]


class PostViewSerializer(ModelSerializer):
    class Meta:
        model = PostView
        fields = ["id", "views", "post"]

class ShipperViewSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "post", "email", "first_name", "last_name", "date_joined", "is_staff"]
