from django.contrib import admin
from .models import Record, Department, Doctor

admin.site.register(Record)
admin.site.register(Doctor)
admin.site.register(Department)
