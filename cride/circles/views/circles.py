from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from cride.circles.models import Circle, MemberShip
from cride.circles.serializers import CircleModelSerializer
from cride.circles.permissions.circles import IsCircleAdmin


class CircleViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    queryset = Circle.objects.all()
    serializer_class = CircleModelSerializer
    #permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        permissions = [IsAuthenticated]

        if self.action in ['update', 'partial_update']:
            permissions.append(IsCircleAdmin)

        return [p() for p in permissions]

    def get_queryset(self):
        queryset = Circle.objects.all()

        if self.action == 'list':
            return queryset.filter(is_public=True)

        return queryset

    def perform_create(self, serializer):
        circle = serializer.save()
        user = self.request.user
        profile = user.profile
        MemberShip.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True,
            remaining_invitations=10
        )
