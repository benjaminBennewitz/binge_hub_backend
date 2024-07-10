from django.contrib import admin
from django.urls import path, include
from main import views
from main.views import LoginView, RegisterView
from django_registration.backends.activation.views import RegistrationView, ActivationView

# URL patterns for the Ticketeer application
# This configuration routes URLs to views.

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Login endpoint
    path('api/bingeHub/login/', views.LoginView.as_view(), name='login'),
    
    # Registration endpoint
    #path('api/bingeHub/register/', views.RegisterView.as_view(), name='register'),
    
    # URLs for django-registration two-step verification
    path('accounts/', include('django_registration.backends.activation.urls')),
    
    # Django Auth URLs for Login, Logout, password change, password reset.
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Endpoint for CSRF-Token
    path('api/get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
]

# Customize specific URLs for django-registration
urlpatterns += [
    path('accounts/register/', views.RegisterView.as_view(), name='django_registration_register'),
    path('accounts/activate/<str:activation_key>/', views.ActivationView.as_view(), name='django_registration_activate'),
]