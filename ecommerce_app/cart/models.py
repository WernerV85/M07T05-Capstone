'''Cart models - Order tracking for purchase verification
Cart is stored in session and will be cleared when session ends.
Orders are tracked in database for purchase verification in reviews.
'''
from django.db import models
from django.conf import settings
from product.models import Product
from rest_framework import serializers


class Order(models.Model):
    """Track customer orders for purchase verification"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='completed'
    )

    def __str__(self):
        """Return a readable label for the order.

        :return: Human-readable order label.
        """
        return f'Order {self.order_id} by {self.user.username}'

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    """Individual products in an order"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """Return a readable label for the order item.

        :return: Human-readable order item label.
        """
        return (
            f'{self.quantity}x {self.product.name} '
            f'in Order {self.order.order_id}'
        )

    def get_total(self):
        return self.quantity * self.price


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 'user', 'created_at', 'total_amount', 'status']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price']
