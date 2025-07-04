from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def create_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)
