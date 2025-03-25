from rest_framework import serializers
from accounts.models import User


class CandidateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "created_at", "is_active"]


class EmployerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "created_at", "is_active"]


class UserActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["is_active"]
