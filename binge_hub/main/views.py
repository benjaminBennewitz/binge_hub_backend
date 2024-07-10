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
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django_registration.backends.activation.views import ActivationView as BaseActivationView
from django.middleware.csrf import get_token
from django.http import JsonResponse


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
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Check if user is activated (assuming 'is_active' is a field in your User model)
        if not user.is_active:
            raise AuthenticationFailed('User account is not activated.')

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
        user = response.data.get('user')  # Assuming your serializer returns 'user' in response data

        # Send activation email
        current_site = get_current_site(request)
        mail_subject = 'Activate your account'
        message = render_to_string('django_registration/activation_email.txt', {
            'user': user,
            'domain': current_site.domain,
            'activation_key': user.registrationprofile.activation_key,
        })
        to_email = user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        return Response({'message': 'Registration successful. Activation email sent.'}, status=response.status_code)
    
    
class ActivationView(BaseActivationView):

    success_url = 'api/bingeHub/accounts/activation_complete/'
    template_name = 'activation.html'
    

def get_csrf_token(request):
    """
    Retrieves the CSRF token for the current session.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        JsonResponse: JSON response containing the CSRF token.
    """
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})