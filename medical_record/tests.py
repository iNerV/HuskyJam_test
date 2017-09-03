from datetime import datetime, date

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from .models import Department, Doctor, Record
from .utils import time_to_str, str_to_time


class MedicalRecordModelTests(TestCase):

    def create_department(self, title="Cardiology",
                          description="This department provides medical care to patients who have problems"
                                      "with their heart or circulation. It treats people on an inpatient and"
                                      "outpatient basis.",
                          from_hour=str_to_time('09:00'),
                          to_hour=str_to_time('18:00'),
                          from_day=0,
                          to_day=4,
                          duration_of_reception=60):
        return Department.objects.create(title=title,
                                         description=description,
                                         from_hour=from_hour,
                                         to_hour=to_hour,
                                         from_day=from_day,
                                         to_day=to_day,
                                         duration_of_reception=duration_of_reception)

    def test_department_creation(self):
        d = self.create_department()
        self.assertTrue(isinstance(d, Department))
        self.assertEqual(d.__str__(), d.title)

    def create_doctor(self, name="House"):
        department = self.create_department()
        return Doctor.objects.create(name=name, department=department)

    def test_doctor_creation(self):
        d = self.create_doctor()
        self.assertTrue(isinstance(d, Doctor))
        self.assertEqual(d.__str__(), d.name)

    def create_record(self, doctor='', full_name='Joe Doe', on_time=str_to_time('11:00'),
                      on_day=date(2017, 8, 28)):
        if doctor == '':
            doctor = self.create_doctor()
        return Record.objects.create(doctor=doctor, full_name=full_name, on_time=on_time, on_day=on_day)

    def test_record_creation(self):
        r = self.create_record()
        self.assertTrue(isinstance(r, Record))
        self.assertEqual(r.__str__(), 'at {hour} on {day} to {doctor}'.format(doctor=r.doctor.name,
                                                                              hour=time_to_str(r.on_time),
                                                                              day=r.on_day))

    def test_record_creation_after_hours(self):
        self.assertRaises(ValidationError, self.create_record, on_time=str_to_time('18:00'))

    def test_record_creation_before_hours(self):
        self.assertRaises(ValidationError, self.create_record, on_time=str_to_time('06:00'))

    def test_record_creation_weekend(self):
        self.assertRaises(ValidationError, self.create_record, on_day=date(2017, 9, 2))

    def test_record_creation_holiday(self):
        department = self.create_department(from_day=6, to_day=1)
        d = Doctor.objects.create(name='Web', department=department)
        self.assertRaises(ValidationError, self.create_record, doctor=d, on_day=date(2017, 8, 28))

    def test_record_creation_during_another_record(self):
        department = self.create_department(duration_of_reception=45)
        d = Doctor.objects.create(name='Watson', department=department)
        self.create_record(doctor=d, on_time=str_to_time('09:00'))
        self.assertRaises(ValidationError, self.create_record, doctor=d, on_time=str_to_time('09:35'))
