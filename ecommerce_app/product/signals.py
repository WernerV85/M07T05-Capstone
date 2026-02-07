from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Product
from ecommerce_app.integrations.x_client import tweet_new_product


@receiver(post_save, sender=Product)
def product_created_tweet(sender, instance, created, **kwargs):
    if created:
        tweet_new_product(instance)
