'''URL patterns for store app
Including:
- URL pattern for store list
- URL pattern for store detail
- URL pattern for store create
- URL pattern for store update
- URL pattern for store delete
'''

from django.urls import path
from . import views

urlpatterns = [
    path('stores/', views.store_list, name='store_list'),
    path('stores/<int:store_id>/', views.store_detail, name='store_detail'),
    path('stores/create/', views.store_create, name='store_create'),
    path('stores/<int:store_id>/update/',
         views.store_update, name='store_update'),
    path('stores/<int:store_id>/delete/',
         views.store_delete, name='store_delete'),
    path('get/stores', views.view_stores),
    path('get/stores/xml', views.view_stores_xml),
    path('add/store', views.add_store),
    path('get/stores/vendor/<int:vendor_id>', views.view_stores_by_vendor),
    path('get/stores/<int:store_id>/products', views.view_products_by_store),
]
