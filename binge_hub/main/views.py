from django import forms
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django_registration.backends.activation.views import ActivationView as BaseActivationView
from django.middleware.csrf import get_token
from django.contrib.auth.forms import PasswordResetForm
from django_registration.backends.activation.views import RegistrationView
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse_lazy
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from django.utils.decorators import method_decorator
from .serializers import VideoSerializer
from .models import Video
from rest_framework.permissions import IsAuthenticated

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

#@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class VideoListView(APIView):
    """
    View to list all videos in the system.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)


    

class CustomRegistrationView(RegistrationView):
    def send_activation_email(self, user):
        """
        Send an activation email to the user with a personalized link.
        """
        activation_key = self.get_activation_key(user)
        current_site = get_current_site(self.request)

        # Generate the activation link
        activation_link = f"{self.request.scheme}://{current_site.domain}/accounts/activate/{activation_key}/"

        # Email context
        context = {
            'user': user,
            'activation_link': activation_link,
        }

        subject = 'Activate your BINGEHUB account'
        html_content = render_to_string('django_registration/activation_email_body.html', context)
        text_content = strip_tags(html_content)  # Fallback for clients that do not support HTML
        from_email = 'bb-dev@outlook.de'
        to_email = user.email

        # Create the email
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")

        # Attach the logo image
        with open('static/media/img/logo.png', 'rb') as img:
            logo = MIMEImage(img.read())
            logo.add_header('Content-ID', '<logo>')
            msg.attach(logo)

        msg.send()
        
        
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
    
    
class CustomActivationView(BaseActivationView):
    """
    Handles the activation of user accounts after registration.

    Attributes:
        template_name (str): The name of the template to render for activation.
    """
    template_name = 'django_registration/activation_complete.html'

    
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
        

class UserPasswordResetForm(PasswordResetForm):
    """
    Custom form for resetting a user's password.
    """
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'})
    )