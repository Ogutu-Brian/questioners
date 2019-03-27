from rest_framework.authentication import get_authorization_header
from users.models import TokenBlacklist
from rest_framework import permissions, status
from rest_framework.response import Response


class TokenAllowedPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        auth = get_authorization_header(request).split()
        token = auth[1]
        granted = None
        try:
            TokenBlacklist.objects.get(token=token)
            granted = False
        except:
            granted = True
        return granted
