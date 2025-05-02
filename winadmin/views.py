from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from accounts.models import User
from .serializers import (
    CandidateListSerializer,
    EmployerListSerializer,
    UserActivationSerializer,
    UserDetailSerializer,
)
from rest_framework.response import Response


class CandidateListView(generics.ListAPIView):
    queryset = User.objects.filter(role="candidate")
    serializer_class = CandidateListSerializer
    permission_classes = [IsAdminUser]


class EmployerListView(generics.ListAPIView):
    queryset = User.objects.filter(role="employer")
    serializer_class = EmployerListSerializer
    permission_classes = [IsAdminUser]


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = "id"
    permission_classes = [IsAdminUser]


class UserActivationView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserActivationSerializer
    lookup_field = "id"
    permission_classes = [IsAdminUser]

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()

        action = "activated" if user.is_active else "deactivated"
        return Response(
            {"message": f"User {user.email} {action} successfully."},
            status=status.HTTP_200_OK,
        )
