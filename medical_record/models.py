from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from datetime import timedelta, time, datetime, date

from .utils import time_to_str, str_to_time

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
    full_name = models.CharField(max_length=30)
    on_time = models.TimeField()
    on_day = models.IntegerField(choices=WEEKDAYS)

    class Meta:
        unique_together = ('doctor', 'on_time', 'on_day')

    def clean(self):
        if self.on_time > self.doctor.department.to_hour or self.on_time < self.doctor.department.from_hour:
            raise ValidationError(_('Out of range time.'))

        if self.on_day < self.doctor.department.from_day or self.on_day > self.doctor.department.to_day:
            raise ValidationError(_('Out of range work days.'))

    def save(self, *args, **kwargs):
        self.clean()
        return super(Record, self).save(*args, **kwargs)

    def __str__(self):
        return 'at {hour} on {day} to {doctor}'.format(doctor=self.doctor.name,
                                                       hour=time_to_str(self.on_time),
                                                       day=self.get_on_day_display())
