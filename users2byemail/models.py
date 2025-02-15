from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.deconstruct import deconstructible
from django.core import validators
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("Email address must be provided.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom user model where email is the unique identifier for authentication
    instead of usernames.
    """
    username = None
    email = models.EmailField(
        unique=True,
        max_length=255,
        validators=[validators.validate_email],
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # No additional fields are required during user creation

    objects = CustomUserManager()
