from django.conf.urls import url
from django.contrib import admin

from medical_record.views import MainPage, SuccessPage, DepartmentList,\
    DepartmentDetail, DoctorDetail, DoctorList

urlpatterns = [
    url(r'^$', MainPage.as_view(), name='main_page'),
    url(r'^success/$', SuccessPage.as_view(), name='success_page'),
    url(r'^departments/$', DepartmentList.as_view(), name='department_list'),
    url(r'^departments/(?P<pk>\d+)/$', DepartmentDetail.as_view(), name='department_detail'),
    url(r'^doctors/$', DoctorList.as_view(), name='doctor_list'),
    url(r'^doctors/(?P<pk>\d+)/$', DoctorDetail.as_view(), name='doctor_detail'),
    url(r'^admin/', admin.site.urls),
]
