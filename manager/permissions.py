from rest_framework import permissions


class IsSuperuser(permissions.BasePermission):
    """
    Permission to only allow access to superusers.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
