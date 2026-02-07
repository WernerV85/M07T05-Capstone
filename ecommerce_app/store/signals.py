from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Store
from ecommerce_app.integrations.x_client import tweet_new_store


@receiver(post_save, sender=Store)
def store_created_tweet(sender, instance, created, **kwargs):
    if created:
        tweet_new_store(instance)
