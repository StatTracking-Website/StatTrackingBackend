from django.db import models

from StatTrackingBackend.models.user_models import User


class Log(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_logs")
    time = models.DateTimeField()
    logger = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_submitted_logs")

    class Meta:
        abstract = True


class CaffeineCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(blank=True, null=True, upload_to='caffeine/')

    def __str__(self):
        return f"{self.name}"


class CaffeineType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(CaffeineCategory, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=256)
    caffeine = models.FloatField()
    commonServing = models.IntegerField()
    image = models.ImageField(blank=True, null=True, upload_to='caffeine/')

    def __str__(self):
        return f"{self.name}"


class CaffeineCommonServing(models.Model):
    name = models.CharField(max_length=50, unique=True)
    value = models.IntegerField()
    image = models.ImageField(blank=True, null=True, upload_to='caffeine/')

    def __str__(self):
        return f"{self.name} - {self.value}ml"


class Caffeine(Log):
    drink_size = models.FloatField()
    drink_type = models.ForeignKey(CaffeineType, related_name="caffeine_logs", on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.person} drank {self.drink_type}"


class TooLate(Log):
    duration = models.IntegerField()
    event = models.CharField(max_length=50)
    excuse = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.person} was {self.duration} minutes too late at {self.event}"


class Horny(Log):
    assault_target = models.CharField(max_length=50)
    assault_type = models.CharField(max_length=50)
    assault_detail = models.CharField(max_length=200)
    assault_intensity = models.SmallIntegerField()

    def __str__(self):
        return f"{self.person} assaulted {self.assault_target}"

