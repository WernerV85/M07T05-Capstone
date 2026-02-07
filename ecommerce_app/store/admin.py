from django.contrib import admin
from .models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('store_id', 'store_name', 'store_category')
    list_filter = ('store_category',)
    search_fields = ('store_name',)
