from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Send activation email
        self.send_activation_email(user)

        return user

    def send_activation_email(self, user):
        subject = 'Activate your account'
        message = 'Please click the link below to activate your account:\n\n' \
                  f'http://localhost:8000/accounts/activate/{user.pk}/'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = user.email
        send_mail(subject, message, from_email, [to_email])
