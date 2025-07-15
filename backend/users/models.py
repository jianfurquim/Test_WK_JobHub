from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def _create_user(self, cpf, email, password, **extra_fields):
        """
        Creates and saves a User with the given CPF, email, and password.
        """
        if not cpf:
            raise ValueError("The CPF field must be set")
        email = self.normalize_email(email)
        user = self.model(
            cpf=cpf, email=email, **extra_fields
        )  # Create the user, passing cpf directly
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, cpf, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(cpf, email, password, **extra_fields)

    def create_superuser(self, cpf, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault(
            "is_active", True
        )  # Superusers should be active by default

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(cpf, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=150, verbose_name="Name")
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")
    email = models.EmailField(
        unique=True, null=True, blank=True, verbose_name="Email"
    )  # Added email, common for superusers

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "cpf"
    REQUIRED_FIELDS = [
        "name"
    ]  # Add 'email' here if you want it to be mandatory during createsuperuser

    objects = CustomUserManager()  # Assign the custom manager to your model

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.name} ({self.cpf})"
