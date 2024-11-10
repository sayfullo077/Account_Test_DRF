from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.db.models import Sum
from rest_framework_simplejwt.tokens import RefreshToken

from common.models import Media
from subject.models import UserTotalTestResult
from .managers import CustomUserManager


class User(AbstractUser, PermissionsMixin):
    class GenderType(models.TextChoices):
        MALE = "male"
        FEMALE = "female"

    class RoleType(models.TextChoices):
        USER = "user"
        TEACHER = "teacher"
    username = models.CharField(max_length=123, null=True, blank=True)
    birth_date = models.DateField("Birth_date", null=True, blank=True)
    photo = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True, related_name="photo")
    email = models.EmailField(unique=True)
    father_name = models.CharField("Father name", max_length=120, null=True, blank=True)
    gender = models.CharField("Gender", choices=GenderType.choices, null=True, blank=True)
    role = models.CharField("Role", choices=RoleType.choices, null=True, blank=True)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        if self.email:
            return f"{self.email}"
        return f"{self.email}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    @property
    def user_total_ball(self):
        filtered_user_results = UserTotalTestResult.objects.filter(user=self)
        total_ball = (
            filtered_user_results.aggregate(total_ball=Sum("ball"))["total_ball"]
            / filtered_user_results.count()
        )

        return total_ball