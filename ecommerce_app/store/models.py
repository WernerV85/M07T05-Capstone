'''defining store model
Includes fields:
- store_id: AutoField (Primary Key)
- store_name: CharField (max_length=100)
- store_category: drop-down selection (max_length=50)
'''

from django.db import models
from django.conf import settings
from rest_framework import serializers


class Store(models.Model):
    STORE_CATEGORIES = [
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('groceries', 'Groceries'),
        ('home_appliances', 'Home Appliances'),
        ('books', 'Books'),
        ('toys', 'Toys'),
    ]

    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=100)
    store_description = models.TextField(blank=True)
    store_category = models.CharField(
        max_length=50,
        choices=STORE_CATEGORIES
    )
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stores',
        limit_choices_to={'user_type': 'vendor'}
    )

    def __str__(self):
        return self.store_name


class StoreSerializer(serializers.ModelSerializer):
    vendor_username = serializers.CharField(
        source='vendor.username', read_only=True
    )

    class Meta:
        model = Store
        fields = [
            'store_id', 'store_name', 'store_description', 'store_category',
            'vendor', 'vendor_username'
        ]
        read_only_fields = ['vendor_username']
