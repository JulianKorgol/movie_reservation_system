from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password as django_validate_password


class UserRegistrationViewSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=8, max_length=128)
    first_name = serializers.CharField(required=True, max_length=64)
    last_name = serializers.CharField(required=True, max_length=64)

    def validate_password(self, password):
        django_validate_password(password)
        return password


class UserEmailConfirmationViewSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    email_confirmation_token = serializers.CharField(required=True, min_length=256, max_length=256)
