import uuid as uuid
from django.db import models

from StatTrackingBackend.models.user_models import User


class Log(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_logs")

    class Meta:
        abstract = True


class SocialLog(Log):
    time = models.DateTimeField()
    logger = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_submitted_logs")

    class Meta:
        abstract = True


class CaffeineCategory(models.Model):
    name = models.CharField(primary_key=True, unique=True, max_length=50)
    image = models.ImageField(blank=True, null=True, upload_to='caffeine/')

    def __str__(self):
        return f"{self.name}"


class CaffeineType(models.Model):
    name = models.CharField(primary_key=True, unique=True, max_length=50)
    category = models.ForeignKey(CaffeineCategory, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=256)
    caffeine = models.FloatField()
    commonServing = models.IntegerField()
    image = models.ImageField(blank=True, null=True, upload_to='caffeine/')

    def __str__(self):
        return f"{self.name}"


class CaffeineCommonServing(models.Model):
    name = models.CharField(primary_key=True, unique=True, max_length=50)
    value = models.IntegerField()
    image = models.ImageField(blank=True, null=True, upload_to='caffeine/')

    def __str__(self):
        return f"{self.name} - {self.value}ml"


class Caffeine(SocialLog):
    drink_size = models.FloatField()
    drink_type = models.ForeignKey(CaffeineType, related_name="caffeine_logs", on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.person} drank {self.drink_type}"


class TooLate(SocialLog):
    duration = models.IntegerField()
    event = models.CharField(max_length=50)
    excuse = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.person} was {self.duration} minutes too late at {self.event}"


class TooLateRating(models.Model):
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name="too_late_ratings")
    target = models.ForeignKey(TooLate, on_delete=models.CASCADE, related_name="ratings_received")
    rating = models.SmallIntegerField()

    class Meta:
        unique_together = ['rater', 'target']


class Sleep(Log):
    date = models.DateField()
    hours_slept = models.FloatField()
    quality = models.SmallIntegerField()

    def __str__(self):
        return f"{self.person} slept {self.hours_slept}"


class MoneyUseCase(models.Model):
    name = models.CharField(primary_key=True, unique=True, max_length=50)
    image = models.ImageField(blank=True, null=True, upload_to='money/')

    def __str__(self):
        return f"{self.name}"


class Money(Log):
    time = models.DateTimeField()
    money_spent = models.FloatField()
    use_case = models.ForeignKey(MoneyUseCase, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.person} slept {self.money_spent}"

