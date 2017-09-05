from django.views.generic import CreateView, DetailView, ListView, TemplateView
from django.urls import reverse

from .models import Department, Doctor
from .forms import RecordForm


class MainPage(TemplateView):
    template_name = 'index.html'


class SuccessPage(TemplateView):
    template_name = 'success.html'


class DepartmentList(ListView):
    model = Department
    template_name = 'medical_record/department_list.html'


class DoctorList(ListView):
    model = Doctor
    template_name = 'medical_record/doctor_list.html'


class DepartmentDetail(DetailView):
    model = Department
    template_name = 'medical_record/department_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DepartmentDetail, self).get_context_data(**kwargs)
        context['doctors'] = self.object.doctors.all()
        return context


class DoctorDetail(CreateView):
    model = Doctor
    template_name = 'medical_record/doctor_detail.html'
    form_class = RecordForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['doctor'] = self.get_object()
        return kwargs

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d['doctor'] = self.get_object()
        return d

    def get_success_url(self):
        return reverse('success_page')
