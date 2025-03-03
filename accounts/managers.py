from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("Invalid email address")

    def _create_user(self, email, password=None, role="candidate"):
        if not email:
            raise ValueError("Users must have an email address")
        self.email_validator(email)
        user = self.model(email=self.normalize_email(email), role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_candidate(self, email, password):
        return self._create_user(email, password, role="candidate")

    def create_employer(self, email, password):
        return self._create_user(email, password, role="employer")

    def create_superuser(self, email, password):
        user = self._create_user(email, password, role="admin")
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
