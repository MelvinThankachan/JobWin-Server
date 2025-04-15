from datetime import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OTP


# @receiver(post_save, sender=OTP)
# def delete_expired_otp(sender, instance, *args, **kwargs):
#     expired_otps = OTP.objects.filter(
#         cool_down_ends_at__lt=timezone.now() - timezone.timedelta(minutes=5)
#     )
#     expired_otps.delete()
