import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from multiselectfield import MultiSelectField

PUBLIC_ACCESS = (('Coffee', 'Access Coffee'),
                 ('TooLate', 'Access Too Late'))
PUBLIC_ACCESS_VALUES = ",".join([i[0] for i in PUBLIC_ACCESS])

HIDDEN_ACCESS = (('Horny', 'Access Horny'),)
HIDDEN_ACCESS_VALUES = ",".join([i[0] for i in HIDDEN_ACCESS])

ACCESS = PUBLIC_ACCESS + HIDDEN_ACCESS
ACCESS_VALUES = ",".join([i[0] for i in ACCESS])


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, user_name, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not user_name:
            raise ValueError('The given user_name must be set')

        user = self.model(user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_name, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(user_name, password, **extra_fields)

    def create_superuser(self, user_name, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(user_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=30, unique=True)
    access = MultiSelectField(choices=ACCESS, max_length=256, default=PUBLIC_ACCESS_VALUES, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.user_name

    @property
    def is_staff(self):
        return self.is_superuser
