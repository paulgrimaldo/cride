from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from cride.users.serializers import (UserLoginSerializer, UserModelSerializer,
                                     UserSignupSerializer, AccountVerificationSerializer)


class UserLoginAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'token': token
        }
        return Response(data, status.HTTP_201_CREATED)


class UserSignUpAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        data = UserModelSerializer(user).data,
        return Response(data, status.HTTP_201_CREATED)


class AccountVerificationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        data = {
            'message': 'Congrations, now go share some rides!'
        }
        return Response(data, status.HTTP_200_OK)
