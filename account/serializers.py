from django.utils import timezone
from rest_framework import serializers

from account.models import User
from common.serializers import MediaURlSerializer


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "role", "email", "password")


class UserSerializer(serializers.ModelSerializer):
    photo = MediaURlSerializer(read_only=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "role", "email", "photo", "birth_date")


class UserProfileSerializer(serializers.ModelSerializer):
    photo = MediaURlSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "father_name",
            "role",
            "email",
            "photo",
            "birth_date",
            "gender",
        )


class ResetPasswordStartSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class ResetPasswordVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get("email")

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email does not exist.")

        return attrs


class SetNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=55)
    new_password = serializers.CharField(min_length=8)
    confirm_password = serializers.CharField(min_length=8)

    def validate(self, attrs):
        email = attrs.get("email")
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        if new_password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email does not exist.")

        return attrs

    def save(self, **kwargs):
        email = self.validated_data.get("email")
        new_password = self.validated_data.get("new_password")
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        return user

class LogoutSerializer(serializers.Serializer):
    model = User
    refresh_token = serializers.CharField(required=True)