from django.contrib import admin
from django.urls import path, include
from main import views
from main.views import LoginView, RegisterView, UserPasswordResetForm
from django_registration.backends.activation.views import RegistrationView, ActivationView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm

# URL patterns for the Ticketeer application
# This configuration routes URLs to views.

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login endpoint
    path('api/bingeHub/login/', views.LoginView.as_view(), name='login'),

    # URLs for django-registration two-step verification
    path('accounts/', include('django_registration.backends.activation.urls')),

    # Django Auth URLs for Login, Logout, password change, password reset.
    path('accounts/', include('django.contrib.auth.urls')),

    # Endpoint for password reset
    path('api/bingeHub/password_reset/', auth_views.PasswordResetView.as_view(template_name='reset_password/password_reset_form.html',form_class=UserPasswordResetForm), name='password_reset'),
    path('api/bingeHub/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password/password_reset_done.html'), name='password_reset_done'),
    path('api/bingeHub/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset_password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('api/bingeHub/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_password/password_reset_complete.html'), name='password_reset_complete'),

    # Endpoint for CSRF-Token
    path('api/bingeHub/get-csrf-token/',
         views.get_csrf_token, name='get_csrf_token'),
]

# Customize specific URLs for django-registration
urlpatterns += [
    path('accounts/register/', views.RegisterView.as_view(),
         name='django_registration_register'),
    path('accounts/activate/<str:activation_key>/',
         views.ActivationView.as_view(), name='django_registration_activate'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
