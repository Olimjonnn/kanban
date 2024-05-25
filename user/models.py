from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

from phonenumber_field.modelfields import PhoneNumberField



class UserManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):
        """
        Creates and saves a User with the given phone number, first name, and password.
        """
        if not phone:
            raise ValueError('Users must have a phone number')

        user = self.model(
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password):
        """
        Creates and saves a superuser with the given phone number and password.
        """
        user = self.create_user(
            phone=phone,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone = PhoneNumberField(region='UZ', unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    EMAIL_FIELD = []

    def __str__(self):
        return self.phone

