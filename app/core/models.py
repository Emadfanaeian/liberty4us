"""Override Default User Behavior"""

from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils.timesince import datetime


class UserManager(BaseUserManager):
    """Custom User Manager"""

    def create_user(self, email, password=None, **extra_fields):
        """create and saves new user"""
        if not email:
            raise ValueError("Email Required")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """ Create SuperUser """
        user = self.create_user(
            email=self.normalize_email(email), password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User Model """
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tags To Be Used For user"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self) -> str:
        return f"{self.name}"


class Countries(models.Model):
    """List Of Countries Model"""
    name = models.CharField(max_length=255)


class Dates(models.Model):
    """List Of Dates And Events"""
    title = models.CharField(max_length=255, null=True)
    date = models.DateField(null=True)


class CountryStates(models.Model):
    """Country States"""
    name = models.CharField(max_length=255)
    country = models.ForeignKey(
        Countries, on_delete=models.SET_NULL, null=True)
    from_date = models.ForeignKey(
        Dates, on_delete=models.SET_NULL, null=True, related_name='form_date')
    to_date = models.ForeignKey(
        Dates, on_delete=models.SET_NULL, null=True, related_name='to_date')
    previous_name = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, related_name='country_states')


class StatesCities(models.Model):
    """States Cities"""
    name = models.CharField(max_length=255)
    state = models.ForeignKey(
        CountryStates, on_delete=models.SET_NULL, null=True)
