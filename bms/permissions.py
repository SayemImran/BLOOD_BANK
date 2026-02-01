from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    Read-only permissions are allowed to any request.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
class IsAdminOnlyDelete(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user and request.user.is_staff
        return True