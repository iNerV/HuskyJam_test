from django.contrib import admin
from django.contrib.admin import SimpleListFilter, ModelAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Record, Department, Doctor


class DoctorFilter(SimpleListFilter):
    title = _('doctor')
    parameter_name = 'doctor'

    def lookups(self, request, model_admin):
        doctors = set([c.doctor for c in model_admin.model.objects.all()])
        return [(c.id, c.name) for c in doctors]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(doctor__id__exact=self.value())
        else:
            return queryset


class RecordAdmin(ModelAdmin):
    list_filter = (DoctorFilter,)

admin.site.register(Record, RecordAdmin)
admin.site.register(Doctor)
admin.site.register(Department)
