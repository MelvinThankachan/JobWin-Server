from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserSignupView, UserLoginView


urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="user_signup"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
