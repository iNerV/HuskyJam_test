from django import forms

from .models import Record


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('full_name', 'on_day', 'on_time')

    def __init__(self, *args, **kwargs):
        self.doctor = kwargs.pop('doctor')
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        record = super().save(commit=False)
        record.doctor = self.doctor
        record.save()
        return record
