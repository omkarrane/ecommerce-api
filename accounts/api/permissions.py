from rest_framework import permissions
from accounts.models import (
    User_Info,
    User_Address,
)


class OwnerPermission(permissions.BasePermission):
    message = "You are not authorised to access this Users data"

    def has_object_permission(self, request, view, obj):
        return (obj.user == request.user)