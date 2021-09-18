from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Category, Good, Post, Place, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "password", "avatar"]
        extra_kwargs = {
            'password' : {'write_only' : 'true'}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class GoodSerializer(ModelSerializer):
    image = SerializerMethodField()

    def get_image(self, good):
        request = self.context['request']
        name = good.image.name
        if name.startswith("static/"):
            path = '/%s' % name
        else:
            path = '/static/%s' % name

        return request.build_absolute_uri(path)


    class Meta:
        model = Good
        fields = ["id", "name", "description", "created_date", "image", "category"]

class PostSerializer(ModelSerializer):

    # image = SerializerMethodField()
    #
    # def get_image(self, post):
    #     request = self.context['request']
    #     name = post.image.name
    #     if name.startswith("static/"):
    #         path = '/%s' % name
    #     else:
    #         path = 'static/%s' % name
    #
    #     return request.build_absolute_uri(path)

    class Meta:
        model = Post
        fields = ["id", "title", "image", "created_date", "content", "user"]

class PlaceSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"