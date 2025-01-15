from rest_framework.generics import CreateAPIView, GenericAPIView
from .models import User
from .serializers import UserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.response import Response


class UserSignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # If the user is candidate he is approved by default
        if user.role == "candidate":
            user.is_approved = True
            user.save()

        # Generating tokens
        refresh = RefreshToken.for_user(user)
        access = AccessToken.for_user(user)

        return Response(
            {
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(access),
            }
        )


class UserLoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        access = AccessToken.for_user(user)

        return Response(
            {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role,
                },
                "refresh": str(refresh),
                "access": str(access),
            }
        )
