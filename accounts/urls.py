from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserSignupView,
    UserLoginView,
    UserLogoutView,
    GenerateOTPView,
    VerifyOTPView,
)


urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="user_signup"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("token-refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", UserLogoutView.as_view(), name="user_logout"),
    path("generate-otp/", GenerateOTPView.as_view(), name="generate-otp"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
]
