from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from users.operations import is_admin


class IsAdmin(BasePermission):
    def has_permission(self, request: Request, _) -> bool:
        return not request.user.is_anonymous and is_admin(request.user.address)
