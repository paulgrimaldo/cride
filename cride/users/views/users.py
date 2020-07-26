from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny, IsAuthenticated)

from cride.users.serializers import (UserLoginSerializer, UserModelSerializer,
                                     UserSignupSerializer, AccountVerificationSerializer)

from cride.users.serializers.profiles import ProfileModelSerializer
from cride.users.models import User
from cride.users.permissions.users import IsAccountOwner
from cride.circles.models import Circle
from cride.circles.serializers import CircleModelSerializer


class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.filter(is_active=True, is_client=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        if self.action in ['signup', 'login', 'verify']:
            permissions = [AllowAny]
        elif self.action == ['retrieve', 'update', 'partial_update']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]

        return [p() for p in permissions]

    @action(detail=False, methods=['POST'])
    def signup(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        data = UserModelSerializer(user).data,
        return Response(data, status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'token': token
        }
        return Response(data, status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def verify(self, request):
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        data = {
            'message': 'Congrations, now go share some rides!'
        }
        return Response(data, status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        circles = Circle.objects.filter(
            members=request.user,
            membership__is_active=True
        )

        data = {
            'user': response.data,
            'circles': CircleModelSerializer(circles, many=True)
        }

        response.data = data
        return response

    @action(detail=True, methods=['PUT', 'PATCH'])
    def profile(self, request, *args, **kwargs):
        user = self.get_object()
        profile = user.profile
        partial = request.method == 'PATCH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data)
