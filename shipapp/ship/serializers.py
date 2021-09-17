from rest_framework.serializers import ModelSerializer
from .models import Good, Post, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "password", "avatar"]
        extra_kwargs =  {
            'password' : {'write_only' : 'true'}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

class GoodSerializer(ModelSerializer):
    class Meta:
        model = Good
        fields = ["id", "name", "description", "created_date", "image", "category"]

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "image", "created_date", "content", "user"]