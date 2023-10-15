from django.db import models

from StatTrackingBackend.models.user_models import User


class Log(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_logs")
    time = models.DateTimeField()
    logger = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_submitted_logs")

    class Meta:
        abstract = True


class Coffee(Log):
    coffee_size = models.FloatField()
    coffee_type = models.CharField(max_length=50)
    coffee_source = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.person} drank {self.coffee_type} from {self.coffee_source}"


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

