from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = "Don't touch someone else's post!"

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
