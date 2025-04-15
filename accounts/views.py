from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import User, OTP
from .serializers import (
    UserSignupSerializer,
    UserLoginSerializer,
    VerifyOTPSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
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

        if user.role == "employer":
            user.is_active = False
            user.save()

        refresh = RefreshToken.for_user(user)
        access = AccessToken.for_user(user)
        user_object = get_user_object(user)

        return Response(
            {
                "user": user_object,
                "refresh": str(refresh),
                "access": str(access),
                "message": "User created successfully",
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
        access = AccessToken.for_user(user)
        user_object = get_user_object(user)

        return Response(
            {
                "user": user_object,
                "refresh": str(refresh),
                "access": str(access),
                "message": "Login successful",
            }
        )


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


class GenerateOTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.is_verified:
            return Response(
                {"detail": "User is already verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp, created = OTP.objects.get_or_create(user=user)
        if otp.is_cool_down():
            error_message = f"Please wait for {(otp.cool_down_ends_at - timezone.now()).total_seconds() // 60:.0f} minutes before generating a new OTP."
            return Response(
                {"otp": error_message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp.generate_otp()
        expires_at_timestamp = int(otp.expires_at.timestamp())
        return Response(
            {"expires_at": expires_at_timestamp, "message": "OTP sent successfully"}
        )


class VerifyOTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = int(serializer.validated_data["otp"])
        user = request.user

        user_otp = OTP.objects.get(user=user)
        print(str(user_otp))
        if not user_otp:
            return Response(
                {"otp": "No OTP found for this user"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if user_otp.is_expired():
            return Response(
                {"otp": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not user_otp.check_otp(otp):
            return Response({"otp": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        if user_otp.check_otp(otp):
            user.is_verified = True
            user.save()
            user_otp.delete()
            return Response(
                {"message": "OTP verified successfully"}, status=status.HTTP_200_OK
            )

        return Response(
            {"otp": "OTP verification failed"}, status=status.HTTP_400_BAD_REQUEST
        )
