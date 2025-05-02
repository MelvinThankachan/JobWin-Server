from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserSignupView,
    UserLoginView,
    UserLogoutView,
    ValidateTokenView,
    PublicVerifyOTPView,
    ResendOTPView,
    AdminLoginView,
)


urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="user_signup"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("admin-login/", AdminLoginView.as_view(), name="admin_login"),
    path("token-refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", UserLogoutView.as_view(), name="user_logout"),
    path("validate-token/", ValidateTokenView.as_view(), name="validate-token"),
    path("verify-otp/", PublicVerifyOTPView.as_view(), name="verify-otp"),
    path("resend-otp/", ResendOTPView.as_view(), name="resend-otp"),
]
