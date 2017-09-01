from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .utils import time_to_str, WEEKDAYS


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
    on_day = models.DateField()

    class Meta:
        unique_together = ('doctor', 'on_time', 'on_day')

    def is_holiday(self, from_day, to_day, day):
        week = [0, 1, 2, 3, 4, 5, 6]
        if from_day > to_day:
            tmp_week = week.copy()
            del tmp_week[to_day+1:from_day]
            for i in tmp_week:
                week.remove(i)
        else:
            tmp_week = week.copy()
            del tmp_week[from_day:to_day+1]
            for i in tmp_week:
                week.remove(i)
        if day.weekday() not in week:
            return True
        return False

    def clean(self):
        if self.on_time.hour >= self.doctor.department.to_hour.hour-1 \
                or self.on_time < self.doctor.department.from_hour:
            raise ValidationError(_('Out of range time.'))

        if self.is_holiday(self.doctor.department.from_day,
                           self.doctor.department.to_day,
                           self.on_day):
            raise ValidationError(_('Out of range work days.'))

    def save(self, *args, **kwargs):
        self.clean()
        return super(Record, self).save(*args, **kwargs)

    def __str__(self):
        return 'at {hour} on {day} to {doctor}'.format(doctor=self.doctor.name,
                                                       hour=time_to_str(self.on_time),
                                                       day=self.on_day)
