from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import User


@receiver(pre_save, sender=User)
def set_user(sender, instance, *args, **kwargs):
    if instance.is_candidate and instance.is_employer:
        raise ValueError("User can't be both candidate and employer")
