from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from .utils import time_to_str, WEEKDAYS


class Department(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    from_hour = models.TimeField()
    to_hour = models.TimeField()
    from_day = models.IntegerField(choices=WEEKDAYS)
    to_day = models.IntegerField(choices=WEEKDAYS)
    duration_of_reception = models.IntegerField()

    def __str__(self):
        return self.title


class Doctor(models.Model):
    name = models.CharField(max_length=30)
    department = models.ForeignKey(Department, related_name='doctors')

    def get_absolute_url(self):
        return reverse('doctor_detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Record(models.Model):
    doctor = models.ForeignKey(Doctor, related_name='records')
    full_name = models.CharField(max_length=30, blank=False)
    on_time = models.TimeField(blank=False)
    on_day = models.DateField(blank=False)

    class Meta:
        unique_together = ('doctor', 'on_time', 'on_day')

    @staticmethod
    def is_holiday(from_day, to_day, day) -> bool:
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

    @staticmethod
    def is_busy(doctor, on_day, on_time) -> bool:
        records = Record.objects.filter(doctor=doctor, on_day=on_day)
        records = map(lambda record: record.on_time, records)
        duration = doctor.department.duration_of_reception
        if records:
            for x in records:
                if on_time.hour == x.hour and on_time.minute in range(x.minute, duration):
                    return True
        return False

    @staticmethod
    def is_late(on_time, doctor) -> bool:
        if on_time.hour >= doctor.department.to_hour.hour-1 \
                or on_time < doctor.department.from_hour:
            return True
        return False

    def clean(self):
        if self.doctor_id is None:
            return

        if self.is_late(self.on_time, self.doctor):
            raise ValidationError(_('Out of range time.'))

        if self.is_holiday(self.doctor.department.from_day,
                           self.doctor.department.to_day,
                           self.on_day):
            raise ValidationError(_('Out of range work days.'))

        if self.is_busy(self.doctor, self.on_day, self.on_time):
            raise ValidationError(_('The time is busy.'))

    def save(self, *args, **kwargs):
        self.clean()
        return super(Record, self).save(*args, **kwargs)

    def __str__(self):
        return 'at {hour} on {day} to {doctor}'.format(doctor=self.doctor.name,
                                                       hour=time_to_str(self.on_time),
                                                       day=self.on_day)
