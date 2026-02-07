from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('prod_id', 'name', 'price', 'store')
    list_filter = ('store',)
    search_fields = ('name', 'description')
