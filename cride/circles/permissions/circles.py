from rest_framework.permissions import BasePermission
from cride.circles.models import MemberShip


class IsCircleAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        try:
            MemberShip.objects.get(
                user=request.user,
                circle=obj,
                is_admin=True,
                is_active=True
            )
        except MemberShip.DoesNotExist:
            return False
        return True
