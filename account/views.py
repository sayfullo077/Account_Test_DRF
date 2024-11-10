from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (
    ResetPasswordVerifySerializer,
    SetNewPasswordSerializer,
    UserProfileSerializer,
    UserRegisterSerializer,
    LogoutSerializer,
)

code = openapi.Parameter(name="code", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
auth_token = openapi.Parameter(
    name="auth_token", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING
)

query = openapi.Parameter(name="query", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        user.set_password(serializer.validated_data["password"])
        user.save()


class UserRegisterVerifyView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        try:

            data = self.serializer_class(data=request.data)
            if not data.is_valid():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"message": "Invalid data"},
                )
            user = User.objects.get(email=data.data["email"])

            user.is_active = True
            user.save()
            return Response(
                status=status.HTTP_200_OK, data={"message": "User is activated"}
            )
        except User.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": "User does not exist"},
            )


class ResetPasswordVerifyView(CreateAPIView):
    serializer_class = ResetPasswordVerifySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"message": "OTP code verified successfully."}, status=status.HTTP_200_OK
        )


class SetNewPasswordView(CreateAPIView):
    serializer_class = SetNewPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Password has been reset successfully."},
            status=status.HTTP_200_OK,
        )


class UserProfileView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = None

    def get_object(self):
        return self.request.user


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=LogoutSerializer)
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data['refresh_token']

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)