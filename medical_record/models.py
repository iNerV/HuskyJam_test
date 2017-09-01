from django.db import models
from django.utils.translation import ugettext_lazy as _

from .utils import time_to_str

WEEKDAYS = [
    (1, _("Monday")),
    (2, _("Tuesday")),
    (3, _("Wednesday")),
    (4, _("Thursday")),
    (5, _("Friday")),
    (6, _("Saturday")),
    (7, _("Sunday")),
]


class Department(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    from_hour = models.TimeField()
    to_hour = models.TimeField()
    from_day = models.IntegerField(choices=WEEKDAYS)
    to_day = models.IntegerField(choices=WEEKDAYS)

    def __str__(self):
        return self.title


class Doctor(models.Model):
    name = models.CharField(max_length=30)
    department = models.ForeignKey(Department)

    def __str__(self):
        return self.name


class Record(models.Model):
    doctor = models.ForeignKey(Doctor)
    on_time = models.TimeField()
    on_day = models.IntegerField(choices=WEEKDAYS)

    class Meta:
        unique_together = ('doctor', 'on_time', 'on_day')

    def __str__(self):
        return 'at {hour} on {day} to {doctor}'.format(doctor=self.doctor.name,
                                                       hour=time_to_str(self.on_time),
                                                       day=self.on_day)
