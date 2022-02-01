from http.client import responses
from operator import mod
from django.shortcuts import render
from accounts import serializers
from accounts.models import User
from rest_framework import viewsets, views, generics, response, status
from accounts.serializers import UserSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import permissions
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    # permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = serializers.RegisterSerializer
    '''
    Set permissions to none.
    To allow register without authorization
    '''
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.initial_data['password'])
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'user_id': user.pk,
                'email': user.email,
                'token': 'Token ' + token.key,
                'is_superuser': user.is_superuser,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
            return response.Response({
                'status': True,
                'message': 'Register Success',
                'data': data,
            }, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(ObtainAuthToken):
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'user_id': user.pk,
                'email': user.email,
                'token': 'Token ' + token.key,
                'is_superuser': user.is_superuser,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
            return response.Response({
                'status': True,
                'message': 'Login Success',
                'data': data,
            }, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return response.Response({
                'status': False,
                'message': 'Invalid E-Mail or Password!',
                's': serializer.errors,
                'data': None,
            }, status=status.HTTP_401_UNAUTHORIZED)
