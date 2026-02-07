'''Define all models for the product.
Include fields:
- prod_id: AutoField (Primary Key)
- name: CharField (max_length=100)
- description: TextField
- price: DecimalField (max_digits=10, decimal_places=2)
- store_id: ForeignKey to Store model
'''

from django.db import models
from store.models import Store
from django.core.validators import MinValueValidator
from rest_framework import serializers


class Product(models.Model):
    prod_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='products'
    )

    def __str__(self):
        return self.name


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['prod_id', 'name', 'description', 'price', 'store']
