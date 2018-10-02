from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from {{ cookiecutter.project_slug }}.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer to handle users."""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password"
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
        }

    def validate_password(self, value):
        value = make_password(value)
        return value


class VerifySerializer(serializers.Serializer):
    """Serializer to verify the user's email."""

    verification_code = serializers.CharField()

    def validate_verification_code(self, value):
        if not User.objects.filter(verification_code=value).exists():
            raise serializers.ValidationError(_("Verification code not found"))
        return value

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class RequestRestoreCodeSerializer(serializers.Serializer):
    """Serializer to request a new password for the user."""

    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("Email not found"))
        return value

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class RestorePasswordSerializer(serializers.Serializer):
    """Serializer to restore a password for the user."""

    password = serializers.CharField()
    repeat_password = serializers.CharField()
    restore_password_code = serializers.CharField()

    def validate_restore_password_code(self, value):
        if not User.objects.filter(restore_password_code=value).exists():
            raise serializers.ValidationError(_("Restore code doesn't exists"))
        return value

    def validate(self, attrs):
        password = attrs.get("password")
        repeat_password = attrs.get("repeat_password")
        if password and repeat_password and password != repeat_password:
            raise serializers.ValidationError(_("Passwords are not the same"))
        return attrs

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
