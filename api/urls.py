from django.urls import path, include

urlpatterns = [
    path("auth/", include("accounts.urls")),
    path("winadmin/", include("winadmin.urls")),
]
