from django.urls import path, include

urlpatterns = [
    path("auth/", include("accounts.urls")),
    path("admin/", include("winadmin.urls")),
]
