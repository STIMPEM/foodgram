from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, recipe):
        return (
            recipe.author == request.user
            or request.method in permissions.SAFE_METHODS
        )