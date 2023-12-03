import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from multiselectfield import MultiSelectField
from django_resized import ResizedImageField

PUBLIC_ACCESS = (('Caffeine', 'Access Caffeine'),
                 ('TooLate', 'Access Too Late'))
PUBLIC_ACCESS_VALUES = ",".join([i[0] for i in PUBLIC_ACCESS])

HIDDEN_ACCESS = (('Horny', 'Access Horny'),)
HIDDEN_ACCESS_VALUES = ",".join([i[0] for i in HIDDEN_ACCESS])

ACCESS = PUBLIC_ACCESS + HIDDEN_ACCESS
ACCESS_VALUES = ",".join([i[0] for i in ACCESS])


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, user_name, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not user_name:
            raise ValueError('The given user_name must be set')

        user = self.model(email=email, user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, user_name, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, user_name, password, **extra_fields)

    def create_superuser(self, email, user_name, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, user_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=30, unique=True)
    access = MultiSelectField(choices=ACCESS, max_length=256, default=PUBLIC_ACCESS_VALUES, blank=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.user_name

    @property
    def is_staff(self):
        return self.is_superuser


class UserVerification(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name="verification")
    verified_email = models.BooleanField(default=False, blank=True)
    email_code = models.CharField(max_length=10, blank=True)
    password_code = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.user_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name="profile")
    picture = ResizedImageField(size=[512, 512], upload_to='profile_pictures/', blank=True, null=True)
    bio = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.user.user_name
