from rest_framework import permissions


class CatalogCreateEditOrReadOnly(permissions.BasePermission):
    edit_create_methods = ("POST", "PUT", "PATCH", "DELETE")

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.user.is_staff and request.method not in self.edit_create_methods:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if obj.created_by == request.user:
            return True

        if request.user.is_staff and request.method in self.edit_create_methods:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return False
