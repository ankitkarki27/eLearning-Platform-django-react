from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

class CustomPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or request.user.is_superuser:
            return True

        if hasattr(obj, "can_change") and callable(getattr(obj, "can_change")):
            return obj.can_change(request.user)

        return False

class IsAdminOrSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_superuser


