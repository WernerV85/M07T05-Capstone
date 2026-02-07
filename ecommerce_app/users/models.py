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
        """Create and save a user with the given credentials.

        :param username: Username for the new user.
        :param email: Email address for the new user.
        :param password: Plain-text password.
        :param extra_fields: Additional fields for the user.
        :return: Created User instance.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Create and save a superuser with the given credentials.

        :param username: Username for the superuser.
        :param email: Email address for the superuser.
        :param password: Plain-text password.
        :param extra_fields: Additional fields for the superuser.
        :return: Created User instance.
        """
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
        """Check if the user has a specific permission.

        :param perm: Permission codename.
        :param obj: Optional object instance.
        :return: True if the user has the permission.
        """
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Check if the user can view the given app.

        :param app_label: Django app label.
        :return: True if the user has module permissions.
        """
        return self.is_superuser

    def __str__(self):
        """Return the display name for the user.

        :return: Username string.
        """
        return self.username


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id', 'first_name', 'last_name', 'username',
            'email', 'user_type', 'is_active'
        ]
        # Exclude password from serialization for security
