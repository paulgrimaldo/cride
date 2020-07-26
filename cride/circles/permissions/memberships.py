from rest_framework.permissions import BasePermission

from cride.circles.models import MemberShip


class IsActiveCircleMember(BasePermission):

    def has_permission(self, request, view):
        try:
            MemberShip.objects.get(
                user=request.user,
                circle=view.circle,
                is_active=True
            )
        except MemberShip.DoesNotExist:
            return False
        return True


class IsSelfMember(BasePermission):

    def has_permission(self, request, view):
        obj = view.get_object()
        return self.has_object_permission(request, view, obj)

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
