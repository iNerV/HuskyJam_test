from django.core.exceptions import ValidationError
from django.forms import ModelForm, SelectDateWidget, TimeInput
from django.utils.translation import ugettext_lazy as _

from .models import Record


class RecordForm(ModelForm):
    class Meta:
        model = Record
        fields = ('full_name', 'on_day', 'on_time')
        widgets = {'on_day': SelectDateWidget(),
                   'on_time': TimeInput}

    def __init__(self, *args, **kwargs):
        self.doctor = kwargs.pop('doctor')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RecordForm, self).clean()

        if Record.is_late(cleaned_data['on_time'], self.doctor):
            raise ValidationError(_('Out of range time.'))

        if Record.is_holiday(self.doctor.department.from_day,
                             self.doctor.department.to_day,
                             cleaned_data['on_day']):
            raise ValidationError(_('Out of range work days.'))

        if Record.is_busy(self.doctor, cleaned_data['on_day'], cleaned_data['on_time']):
            raise ValidationError(_('The time is busy.'))

    def save(self, *args, **kwargs):
        record = super().save(commit=False)
        record.doctor = self.doctor
        record.save()
        return record
