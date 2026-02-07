'''URL patterns for users app
Including:
- URL pattern for user registration
- URL pattern for user login
'''

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/',
         views.password_reset_request, name='password_reset_request'),
    path('reset-password/<uidb64>/<token>/',
         views.password_reset_confirm, name='password_reset_confirm'),
    path('get/users', views.view_users),
    path('get/users/xml', views.view_users_xml),
    path('api/register', views.register_user),
]
