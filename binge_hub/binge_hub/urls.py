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
    path('api/bingeHub/register/', views.RegisterView.as_view(), name='register'),
    
    # URLs für die django-registration Two-Step-Verifizierung
    path('accounts/', include('django_registration.backends.activation.urls')),
    
    # Django Auth URLs für Login, Logout, Passwort ändern, Passwort zurücksetzen usw.
    path('accounts/', include('django.contrib.auth.urls')),
]

# Spezifische URLs für django-registration anpassen
urlpatterns += [
    path('accounts/register/', views.RegisterView.as_view(), name='django_registration_register'),  # Hier sollte views.RegisterView verwendet werden, falls es eine spezielle View dafür gibt
    path('accounts/activate/<str:activation_key>/', views.ActivationView.as_view(), name='django_registration_activate'),  # Hier sollte views.ActivationView verwendet werden
]