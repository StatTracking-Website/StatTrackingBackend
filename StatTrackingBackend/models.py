from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from multiselectfield import MultiSelectField

USER_RIGHTS = (('Coffee', 'Access Coffee'),
               ('TooLate', 'Access Too Late'),
               ('Horny', 'Access Horny'))


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
    user_name = models.CharField(max_length=30, unique=True)
    # token = models.CharField(max_length=20)

    objects = UserManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.user_name

    @property
    def is_staff(self):
        return self.is_superuser


class Log(models.Model):
    logger = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_submitted_logs")
    time = models.DateTimeField()
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_logs")

    class Meta:
        abstract = True
        default_permissions = ("access", )


class Coffee(Log):
    coffee_size = models.FloatField()
    coffee_type = models.CharField(max_length=50)
    coffee_source = models.CharField(max_length=50)


class TooLate(Log):
    duration = models.IntegerField()
    event = models.CharField(max_length=50)
    excuse = models.CharField(max_length=200)


class Horny(Log):
    assault_target = models.CharField(max_length=50)
    assault_type = models.CharField(max_length=50)
    assault_detail = models.CharField(max_length=200)
    assault_intensity = models.SmallIntegerField()