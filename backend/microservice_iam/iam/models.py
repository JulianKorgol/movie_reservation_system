import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


'''
USER
'''


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('status', 1)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = None
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.IntegerField(default=3, choices=(
        (1, 'Active'),
        (2, 'Suspended'),
        (3, "Pending Activation")
    ))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    is_active = None

    @property
    def is_active(self):
        return self.status == 1

    objects = CustomUserManager()

    def __str__(self):
        return self.email


'''
END USER
'''


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='details')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True, editable=False)
    country = models.CharField(max_length=3,
                               help_text="Reference: Location.Country.code")  # Reference to external microservice

    class Meta:
        verbose_name_plural = "User Details"

    def __str__(self):
        return f"Details for {self.user.email}"


class RefreshToken(models.Model):
    token_hash = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refresh_token')
    issued_at = models.DateTimeField(auto_now_add=True, editable=False)
    issued_ip = models.GenericIPAddressField(null=True, blank=True)
    expires_at = models.DateTimeField()
    is_revoked = models.BooleanField(default=False)

    def __str__(self):
        return f"Token for {self.user.email} (Exp: {self.expires_at})"


class ObjectStorageServer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_signed_url_required = models.BooleanField(default=False)
    domain = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}: {self.domain}"
