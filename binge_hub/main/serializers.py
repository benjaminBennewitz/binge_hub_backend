from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Video model.

    This serializer is used to convert Video model instances into JSON format
    and validate incoming data for creating or updating Video instances.
    """
    class Meta:
        model = Video
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    This serializer is used to handle user registration by validating the input data
    and creating a new User instance.

    Attributes:
        email (EmailField): 
            Email address of the user, must be valid and unique.
    """
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user