from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    UserRegisterVerifyView,
    UserRegisterView,
    ResetPasswordVerifyView,
    SetNewPasswordView,
    UserProfileView,
    LogoutAPIView,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("register/verify/", UserRegisterVerifyView.as_view(), name="register-verify"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("user/profile", UserProfileView.as_view(), name="profile"),
    path("reset-password/verify/", ResetPasswordVerifyView.as_view(), name="reset-password-verify",),
    path("reset-password/set/", SetNewPasswordView.as_view(), name="reset-password-set"),
]