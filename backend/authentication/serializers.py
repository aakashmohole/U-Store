from rest_framework import serializers
from .models import Users 
from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator

#USerSerializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id", "name", "email", "phone_number", "address", "user_type"]

#user register serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ["name", "email", "password", "phone_number", "address", "user_type"]

    def create(self, validated_data):
        user = Users.objects.create_user(**validated_data)
        return user

#Login serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
 
# Password Rseset Serializer   
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Check if the email exists in the Users model
        user = Users.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError("User with this email does not exist.")

        # Generate password reset token
        token = default_token_generator.make_token(user)
        reset_url = f"http://localhost:3000/reset-password/{user.pk}/{token}/"

        # Ensure email settings are loaded
        if not settings.EMAIL_HOST_USER:
            raise ValueError("EMAIL_HOST_USER is not set. Check your .env file.")

        # Send password reset email
        send_mail(
            "Password Reset Request",
            f"Click the link below to reset your password:\n{reset_url}",
            settings.EMAIL_HOST_USER,
            [value],
            fail_silently=False,
        )

        return value