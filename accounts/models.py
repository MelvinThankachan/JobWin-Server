from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ("temporary", "Temporary"),
        ("candidate", "Candidate"),
        ("company", "Company"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="temporary")
    is_approved = models.BooleanField(default=False)
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
    def is_company(self):
        return self.role == "employer"

    @property
    def is_temporary(self):
        return self.role == "temporary"
