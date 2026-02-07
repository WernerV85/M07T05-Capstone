'''User views for authentication
Includes:
- User registration
- User login
'''

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User, UserSerializer
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import (
    api_view, renderer_classes, authentication_classes, permission_classes
)
from rest_framework.response import Response
from rest_framework_xml.renderers import XMLRenderer
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser


def register(request):
    """Register a new user via the HTML form.

    :param request: Django HttpRequest.
    :return: Rendered response or redirect.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                user_type=form.cleaned_data['user_type']
            )
            user.save()
            messages.success(
                request,
                'Account created successfully! Please login.'
            )
            return redirect('login')

        return render(request, 'register.html', {'form': form})

    form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """Authenticate and log in a user.

    :param request: Django HttpRequest.
    :return: Rendered response or redirect.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            return render(
                request,
                'login.html',
                {'error': 'Invalid username or password'}
            )

    return render(request, 'login.html')


def logout_view(request):
    """Log out the current user.

    :param request: Django HttpRequest.
    :return: Redirect response.
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def password_reset_request(request):
    """Send a password reset link to the user email.

    :param request: Django HttpRequest.
    :return: Rendered response or redirect.
    """
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            # Generate token and uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Build reset URL (expires in 2 hours - settings)
            reset_url = (
                f"{request.scheme}://{request.get_host()}"
                f"/reset-password/{uid}/{token}/"
            )

            # Send email
            email_subject = 'Password Reset Request'
            email_body = f'''Hello {user.username},

You requested to reset your password. Click the link below to reset it:

{reset_url}

This link will expire in 2 hours.

If you did not request this, please ignore this email.

Best regards,
eCommerce Team
'''

            send_mail(
                subject=email_subject,
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(
                request,
                'Password reset link has been sent to your email.'
            )
            return redirect('login')

        except User.DoesNotExist:
            # Don't reveal if email exists for security
            messages.success(
                request,
                'If that email exists, a password reset link has '
                'been sent.'
            )
            return redirect('login')

    return render(request, 'password_reset_request.html')


def password_reset_confirm(request, uidb64, token):
    """Confirm password reset with token validation.

    :param request: Django HttpRequest.
    :param uidb64: Base64-encoded user id.
    :param token: Password reset token.
    :return: Rendered response or redirect.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Check if token is valid (automatically checks 2-hour expiration)
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password1 != password2:
                messages.error(request, 'Passwords do not match.')
                return render(
                    request,
                    'password_reset_confirm.html',
                    {'validlink': True}
                )

            # Set new password
            user.set_password(password1)
            user.save()

            messages.success(
                request,
                'Your password has been reset successfully! '
                'Please login.'
            )
            return redirect('login')

        return render(
            request,
            'password_reset_confirm.html',
            {'validlink': True}
        )
    else:
        messages.error(
            request,
            'Password reset link is invalid or has expired.'
        )
        return render(
            request,
            'password_reset_confirm.html',
            {'validlink': False}
        )


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def view_users(request):
    """Return all users in JSON format (admin only).

    :param request: Django HttpRequest.
    :return: JsonResponse with users.
    """
    serializer = UserSerializer(User.objects.all(), many=True)
    return JsonResponse(data=serializer.data, safe=False)


@api_view(['GET'])
@renderer_classes([XMLRenderer])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def view_users_xml(request):
    """Return all users in XML format (admin only).

    :param request: Django HttpRequest.
    :return: DRF Response with users.
    """
    serializer = UserSerializer(User.objects.all(), many=True)
    return Response(data=serializer.data)


@api_view(['POST'])
def register_user(request):
    """Register a new user via the API.

    :param request: Django HttpRequest.
    :return: JsonResponse with user data or errors.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Create user using UserManager to handle password hashing
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=request.data.get('password'),
            first_name=serializer.validated_data.get('first_name', ''),
            last_name=serializer.validated_data.get('last_name', ''),
            user_type=serializer.validated_data['user_type']
        )
        response_serializer = UserSerializer(user)
        return JsonResponse(
            data=response_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(
        data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
