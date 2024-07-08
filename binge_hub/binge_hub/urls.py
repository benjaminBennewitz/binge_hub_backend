from django.contrib import admin
from django.urls import path

from bingeHub import views
from bingeHub.views import LoginView, RegisterView

# URL patterns for the Ticketeer application
# This configuration routes URLs to views.

urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),

    # Login endpoint
    path('api/bingeHub/login/', views.LoginView.as_view(), name='login'),

    # Registration endpoint
    path('api/bingeHub/register/', views.RegisterView.as_view(), name='register'),

    # Endpoint for overview
    #path('overview/', views.StreamView.as_view(), name='overview'),
]