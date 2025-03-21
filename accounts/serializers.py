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
        email = validated_data.get("email").lower()
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
    role = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email").lower()
        password = attrs.get("password")
        role = attrs.get("role")

        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError(
                {"email": "User with this email does not exist"}
            )

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Incorrect password"})

        if user.role != role:
            raise serializers.ValidationError({"role": "Invalid role for this user"})

        if not user.is_active:
            raise serializers.ValidationError(
                {"email": "This account is inactive, please contact the administrator"}
            )

        attrs["user"] = user
        return attrs
