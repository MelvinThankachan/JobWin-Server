from rest_framework import permissions


class IsCandidate(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_candidate


class IsCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_company


class IsSuperAdmin(permissions.BasePermission):
    print("Superuser auth out")

    def has_permission(self, request, view):
        print("Superuser auth in")
        access = request.user and request.user.is_superuser
        print(access)
        return access
