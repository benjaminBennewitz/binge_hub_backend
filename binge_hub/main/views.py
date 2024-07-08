from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class LoginView(ObtainAuthToken):
    """
    Custom login view to authenticate users and generate tokens.
    Inherits:
        ObtainAuthToken: Base class to obtain authentication tokens.
    """
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to authenticate users.
        Args:
            request: HTTP request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            Response: JSON response containing authentication token and user details.
        """
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        
        
class RegisterView(generics.CreateAPIView):
    """
    View for user registration.
    Attributes:
        serializer_class: Serializer class for user registration.
        permission_classes: Permissions required for accessing this view (none for registration).
    """

    serializer_class = RegisterSerializer
    permission_classes = []  # No authentication necessary for registration

    def create(self, request, *args, **kwargs):
        """
        Handle POST requests for user registration.
        Args:
            request: HTTP request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            Response: JSON response indicating success or failure of registration.
        """
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Registration successful'}, status=response.status_code)