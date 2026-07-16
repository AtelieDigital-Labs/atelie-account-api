from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("O usuário precisa ter um username")
        if not email:
            raise ValueError("O usuário precisa ter um email")

        email = self.normalize_email(email)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_artisan", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser precisa ter is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser precisa ter is_superuser=True")

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(unique=True, max_length=50)
    email = models.EmailField(unique=True, max_length=255)
    cpf = models.CharField(max_length=11, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to="images", null=True)
    bio = models.TextField(null=True)
    is_artisan = models.BooleanField(default=False)

    # campos obrigatórios
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"  # login por username
    REQUIRED_FIELDS = ["username"]  # exigido ao criar superuser

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"
        constraints = [
            models.UniqueConstraint(
                fields=["cpf"], condition=~Q(cpf=None), name="unique_cpf_not_null"
            )
        ]
