from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django_registration.backends.activation.views import ActivationView as BaseActivationView
from django.middleware.csrf import get_token
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.views.generic import View



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
        
        # Check if user is activated (assuming 'is_active' is a field in the User model)
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

    success_url = 'accounts/activation_complete/'
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


class PasswordResetConfirmView(View):
    def post(self, request, uidb64, token):
        # Entschlüsseln der Benutzer-ID und Überprüfung des Tokens
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            # Token ist gültig, speichere das neue Passwort
            new_password = request.POST.get('password')
            user.set_password(new_password)
            user.save()
            return redirect('password_reset_complete')  # Weiterleitung zur Bestätigungsseite
        else:
            # Token ungültig oder Benutzer nicht gefunden
            return redirect('password_reset_invalid')  # Weiterleitung zur Fehlerseite