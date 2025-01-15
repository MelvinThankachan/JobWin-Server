from rest_framework import serializers
from .models import User
from .validators import CustomPasswordValidator
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "role", "password")
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ("id",)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate_password(self, value):
        CustomPasswordValidator().validate(value)
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Invalid email")

        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid password.")

        attrs["user"] = user
        return attrs
