'''Model to define the review structure for products.
Includes fields:
- review_id: AutoField (Primary Key)
- product_id: ForeignKey to Product model
- user_id: ForeignKey to User model
- username: CharField (max_length=150)
- rating: IntegerField (1 to 5)
- comment: TextField
- created_at: DateTimeField (auto_now_add=True)
'''

from django.db import models
from product.models import Product
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    username = models.CharField(max_length=150)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified_purchase = models.BooleanField(
        default=False,
        help_text='True if the user purchased this product'
    )

    def __str__(self):
        return (
            f'Review {self.review_id} by {self.username} '
            f'for {self.product.name}'
        )

    def check_verified_purchase(self):
        """Check if the user who wrote this review purchased the product"""
        from cart.models import OrderItem
        return OrderItem.objects.filter(
            order__user=self.user,
            product=self.product,
            order__status='completed'
        ).exists()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'review_id', 'product', 'user', 'username',
            'rating', 'comment', 'created_at', 'is_verified_purchase'
        ]
