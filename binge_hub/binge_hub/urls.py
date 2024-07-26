from django.contrib import admin
from django.urls import path, include
from main import views
from main.views import CustomActivationView, CustomRegistrationView, LoginView, UserPasswordResetForm, VideoListView
from django_registration.backends.activation.views import RegistrationView, ActivationView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm
from django.views.generic import TemplateView
from debug_toolbar.toolbar import debug_toolbar_urls

# URL patterns for the BINGEHUB application
# This configuration routes URLs to views.

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login endpoint
    path('api/bingeHub/login/', views.LoginView.as_view(), name='login'),
    # Videos endpoint
    path('api/bingeHub/videos/', VideoListView.as_view(), name='video-list'),

    # Registration view
    path('accounts/register/', CustomRegistrationView.as_view(), name='django_registration_register'),
    # Activation view
    path('accounts/activate/<str:activation_key>/', CustomActivationView.as_view(), name='activation_complete'),
    # Include the default django-registration URLs
    path('accounts/', include('django_registration.backends.activation.urls')),
  

    # Django Auth URLs for Login, Logout, password change, password reset.
    path('accounts/', include('django.contrib.auth.urls')),
    # Endpoint for password reset
    path('api/bingeHub/password_reset/', auth_views.PasswordResetView.as_view(template_name='reset_password/password_reset_form.html',form_class=UserPasswordResetForm), name='password_reset'),
    path('api/bingeHub/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password/password_reset_done.html'), name='password_reset_done'),
    path('api/bingeHub/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset_password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('api/bingeHub/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_password/password_reset_complete.html'), name='password_reset_complete'),

    # Endpoint for CSRF-Token
    path('api/bingeHub/get-csrf-token/',views.get_csrf_token, name='get_csrf_token'),
    
    # Django-RQ
    path('django-rq/', include('django_rq.urls'))
]   + debug_toolbar_urls()

# set static folder
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
