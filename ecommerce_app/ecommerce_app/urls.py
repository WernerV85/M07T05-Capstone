"""
URL configuration for ecommerce_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/5.2/topics/http/urls/

Examples:

Function views::

    from my_app import views
    path('', views.home, name='home')

Class-based views::

    from other_app.views import Home
    path('', Home.as_view(), name='home')

Including another URLconf::

    from django.urls import include, path
    path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


def home(request):
    """Render the homepage.

    :param request: Django HttpRequest.
    :return: Rendered homepage.
    """
    return render(request, 'home.html')


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
]

''' Including URL patterns from product, store, and reviews apps
into the main ecommerce_app URL configuration.
'''

urlpatterns += [
    path('', include('users.urls')),
    path('', include('product.urls')),
    path('', include('store.urls')),
    path('', include('reviews.urls')),
    path('cart/', include('cart.urls')),
]
