from rest_framework import serializers
from .models import User, OTP
from .validators import CustomPasswordValidator
from django.contrib.auth import authenticate


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "role", "password")
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ("id",)

    def create(self, validated_data):
        validated_data["email"] = validated_data.get("email").lower()
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate_password(self, value):
        CustomPasswordValidator().validate(value)
        return value


class UserLoginSerializer(serializers.Serializer):
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

        # if not user.is_active:
        #     raise serializers.ValidationError(
        #         {"email": "This account is inactive, please contact the administrator"}
        #     )

        attrs["user"] = user
        return attrs


class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(min_length=6, max_length=6)

    def validate_otp(self, value):
        if not str(value).isdigit() or len(str(value)) != 6:
            raise serializers.ValidationError("OTP must be a 6-digit number")
        return value


class PublicVerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(min_length=6, max_length=6)
    verification_token = serializers.CharField(required=False)

    def validate_otp(self, value):
        if not str(value).isdigit() or len(str(value)) != 6:
            raise serializers.ValidationError("OTP must be a 6-digit number")
        return value

    def validate(self, attrs):
        email = attrs.get("email").lower()
        verification_token = attrs.get("verification_token")
        otp = attrs.get("otp")

        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError(
                {"email": "User with this email does not exist"}
            )

        otp_instance = OTP.objects.filter(user=user).first()
        if not otp_instance:
            raise serializers.ValidationError({"email": "User has no OTP instance"})

        if not otp_instance.check_otp(otp):
            raise serializers.ValidationError({"otp": "Incorrect OTP"})

        if (
            verification_token
            and otp_instance.verification_token
            and verification_token != otp_instance.verification_token
        ):
            raise serializers.ValidationError(
                {"verification_token": "Invalid verification token"}
            )

        attrs["user"] = user
        return attrs


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email").lower()
        password = attrs.get("password")

        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError(
                {"email": "User with this email does not exist"}
            )
        
        if user.role != "admin":
            raise serializers.ValidationError(
                {"email": "Access denied. Admin privileges required."}
            )

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Incorrect password"})


        attrs["user"] = user
        return attrs
