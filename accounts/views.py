from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import User, OTP
from .serializers import (
    UserSignupSerializer,
    UserLoginSerializer,
    PublicVerifyOTPSerializer,
    ResendOTPSerializer,
    AdminLoginSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .utils import get_user_object
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken


class UserSignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user.is_verified = False

        if user.role == "employer":
            user.is_active = False

        user.save()

        otp, created = OTP.objects.get_or_create(user=user)
        otp.generate_otp()

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        user_object = get_user_object(user)

        return Response(
            {
                "user": user_object,
                "refresh": str(refresh),
                "access": str(access),
                "message": "User created successfully. Please verify your email with the OTP sent.",
                "is_verified": False,
                "verification_token": otp.verification_token,
            },
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        OutstandingToken.objects.filter(user=user).delete()
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        user_object = get_user_object(user)

        response_data = {
            "user": user_object,
            "refresh": str(refresh),
            "access": str(access),
            "message": "Login successful",
        }

        if not user.is_verified:
            otp, created = OTP.objects.get_or_create(user=user)
            if created or not otp.verification_token:
                otp.generate_otp()

            response_data["verification_token"] = otp.verification_token

        return Response(response_data)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response(
                    {"message": "Successfully logged out"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"detail": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ValidateTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_object = get_user_object(user)

        return Response({"valid": True, "user": user_object}, status=status.HTTP_200_OK)


class PublicVerifyOTPView(APIView):
    def post(self, request):
        serializer = PublicVerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp_code = serializer.validated_data["otp"]
        verification_token = serializer.validated_data.get("verification_token")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"otp": "User with this email does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            user_otp = OTP.objects.get(user=user)
        except OTP.DoesNotExist:
            return Response(
                {"otp": "No OTP found for this user. Please request a new OTP."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if (
            verification_token
            and user_otp.verification_token
            and user_otp.verification_token != verification_token
        ):
            return Response(
                {"otp": "Invalid verification token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user_otp.is_expired():
            return Response(
                {"otp": "OTP has expired. Please request a new OTP."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user_otp.check_otp(otp_code):
            return Response(
                {"otp": "Invalid OTP. Please check and try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.is_verified = True
        user.save()

        user_otp.delete()

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response(
            {
                "message": "Email verified successfully.",
                "user": get_user_object(user),
                "refresh": str(refresh),
                "access": str(access),
                "is_verified": True,
            },
            status=status.HTTP_200_OK,
        )


class AdminLoginView(GenericAPIView):
    serializer_class = AdminLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        
        # Clear any existing tokens for this user
        OutstandingToken.objects.filter(user=user).delete()
        
        # Generate new JWT tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        user_object = get_user_object(user)

        return Response(
            {
                "user": user_object,
                "refresh": str(refresh),
                "access": str(access),
                "message": "Admin login successful",
            },
            status=status.HTTP_200_OK,
        )


class ResendOTPView(APIView):
    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "User with this email does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if user.is_verified:
            return Response(
                {"detail": "User is already verified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp, created = OTP.objects.get_or_create(user=user)

        # Check if the OTP is in cool down period
        if otp.is_cool_down():
            remaining_seconds = (otp.cool_down_ends_at - timezone.now()).total_seconds()
            minutes = int(remaining_seconds // 60)
            seconds = int(remaining_seconds % 60)

            return Response(
                {
                    "otp": f"Please wait for {minutes} minutes and {seconds} seconds before requesting a new OTP.",
                    "cool_down_ends_at": int(otp.cool_down_ends_at.timestamp()),
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        if (
            not otp.is_expired()
            and otp.otp is not None
            and otp.verification_token is not None
        ):
            return Response(
                {
                    "message": "A valid OTP already exists and has been sent to your email.",
                    "expires_at": int(otp.expires_at.timestamp()),
                    "verification_token": otp.verification_token,
                },
                status=status.HTTP_200_OK,
            )

        otp.generate_otp()

        return Response(
            {
                "message": "OTP sent successfully.",
                "expires_at": int(otp.expires_at.timestamp()),
                "verification_token": otp.verification_token,
            },
            status=status.HTTP_200_OK,
        )
