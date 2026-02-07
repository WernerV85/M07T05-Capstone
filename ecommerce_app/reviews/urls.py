'''URL patterns for reviews app
Including:
- URL pattern for listing reviews
- URL pattern for review detail
- URL pattern for creating a review
'''

from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/<int:review_id>/',
         views.review_detail, name='review_detail'),
    path('reviews/create/', views.review_create, name='review_create'),
    path('get/reviews', views.view_reviews),
    path('get/reviews/xml', views.view_reviews_xml),
    path('add/review', views.add_review),
]
