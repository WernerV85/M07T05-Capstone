'''model to define user structure.
Includes fields:
- user_id: AutoField (Primary Key)
- first_name: CharField (max_length=30)
- last_name: CharField (max_length=30)
- username: CharField (max_length=150)
- email: EmailField (unique=True)
- password: CharField (max_length=128)
- user_type: drop-down selection (max_length=50)
'''
# include validators for email and password strength
# password to include at least one uppercase and one digit
# encrypt password before saving to database
# encryption using Django's built-in password hashing

from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework import serializers


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser):
    USER_TYPES = [
        ('buyer', 'Buyer'),
        ('vendor', 'Vendor'),
    ]

    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    password = models.CharField(
        max_length=128,
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*\d).+$',
                message=(
                    'Password must contain at least one uppercase '
                    'letter and one digit.'
                )
            )
        ]
    )
    user_type = models.CharField(
        max_length=50,
        choices=USER_TYPES
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'user_type']

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return self.is_superuser

    def __str__(self):
        return self.username


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id', 'first_name', 'last_name', 'username',
            'email', 'user_type', 'is_active'
        ]
        # Exclude password from serialization for security
