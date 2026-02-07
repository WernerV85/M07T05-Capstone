'''URL patterns for cart app
Including:
- Add to cart
- View cart
- Update cart item
- Remove from cart
- Checkout
'''
from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart_view'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('checkout/', views.cart_checkout, name='cart_checkout'),
    path('get/orders', views.view_orders),
    path('get/orders/xml', views.view_orders_xml),
    path('add/order', views.add_order),
]
