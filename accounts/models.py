from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from random import randint
from django.utils import timezone
from .utils import send_otp
from django.conf import settings


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ("candidate", "Candidate"),
        ("employer", "Employer"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="candidate")
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.is_superuser

    @property
    def is_candidate(self):
        return self.role == "candidate"

    @property
    def is_employer(self):
        return self.role == "employer"

    @property
    def is_temporary(self):
        return self.role == "temporary"


class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="otp")
    otp = models.PositiveIntegerField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    generations = models.PositiveIntegerField(default=0)
    cool_down_ends_at = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        return f"OTP for {self.user.email} - {self.otp}"

    def is_expired(self):
        return timezone.now() > self.expires_at

    def is_cool_down(self):
        if self.cool_down_ends_at is None:
            return False
        return timezone.now() < self.cool_down_ends_at

    def generate_otp(self):
        # cool down reset
        if self.is_cool_down():
            raise Exception("Cool down period not over yet")
        if self.cool_down_ends_at is not None and not self.is_cool_down():
            self.generations = 0
            self.cool_down_ends_at = None

        self.otp = randint(100000, 999999)
        self.expires_at = timezone.now() + timezone.timedelta(
            minutes=settings.OTP_EXPIRATION_TIME
        )
        self.generations += 1
        if self.generations >= settings.OTP_MAX_GENERATIONS:
            self.cool_down_ends_at = timezone.now() + timezone.timedelta(
                minutes=settings.OTP_COOL_DOWN_TIME
            )
        send_otp(self.user.email, self.otp)
        self.save()

    def check_otp(self, otp):
        return self.otp == otp
