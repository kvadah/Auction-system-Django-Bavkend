from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import ValidationError
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email already in use")
        return value

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super(RegisterSerializer, self).create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
