from django.urls import path
from .views import CandidateListView, EmployerListView, UserActivationView, UserDetailView


urlpatterns = [
    path("candidates/", CandidateListView.as_view(), name="candidate-list"),
    path("employers/", EmployerListView.as_view(), name="employer-list"),
    path("user/<int:id>/", UserDetailView.as_view(), name="user-detail"),
    path(
        "user/<int:id>/activation/", UserActivationView.as_view(), name="user-activation"
    ),
]
