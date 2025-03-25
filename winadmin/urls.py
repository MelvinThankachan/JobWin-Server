from django.urls import path
from .views import CandidateListView, EmployerListView, UserActivationView


urlpatterns = [
    path("candidates/", CandidateListView.as_view(), name="candidate-list"),
    path("employers/", EmployerListView.as_view(), name="employer-list"),
    path(
        "user/<int:id>/activate/", UserActivationView.as_view(), name="user-activation"
    ),
]
