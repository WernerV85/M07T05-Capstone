''' Module for defining urls patterns for product app
Including:
- URL pattern for product list
- URL pattern for product detail
- URL pattern for product create
- URL pattern for product update
- URL pattern for product delete
'''

from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/<int:prod_id>/',
         views.product_detail, name='product_detail'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:prod_id>/update/',
         views.product_update, name='product_update'),
    path('products/<int:prod_id>/delete/',
         views.product_delete, name='product_delete'),
    path('get/products', views.view_products),
    path('get/products/xml', views.view_products_xml),
    path('add/product', views.add_product),
]
